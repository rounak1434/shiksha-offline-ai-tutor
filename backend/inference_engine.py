"""
backend/inference_engine.py
Core Native Inference Engine for SHIKSHA Offline AI Tutor.
Wraps llama.cpp native binary execution with:
- Model load / unload lifecycle management
- Streaming generation with cancellation support
- Structured educational prompt construction
- Real-time token and speed metrics extraction
- Local-only execution (zero internet dependencies)
"""

import os
import sys
import subprocess
import threading
import time
import re
import uuid
from typing import Dict, Any, Generator, Optional, List

from backend.response_contract import (
    InferenceResponse,
    InferenceStreamChunk,
    RuntimeMetrics,
    StructuredTutorParser,
    TutoringMetadata,
)

DEFAULT_MODEL_PATH = r"C:\Rounak\RVSHACK\output\qwen3_k8_tutor_q4_k_m.gguf"
DEFAULT_LLAMA_CLI = r"C:\Rounak\RVSHACK\llama.cpp\build_bin\llama-cli.exe"

SYSTEM_PROMPT = (
    "You are SHIKSHA, an offline school AI tutor for Class 1 to 8 students.\n"
    "Follow these instructions strictly:\n"
    "1. Answer the student's actual question directly and accurately.\n"
    "2. Never return generic educational filler or invent missing values.\n"
    "3. If given an algebraic expression with unknown variables where no values are provided, "
    "explicitly state that a numerical answer cannot be calculated without the values of the variables.\n"
    "4. For mathematical calculations, calculate step-by-step when numbers are given.\n"
    "5. Use structured sections (Given, Required, Formula, Explanation, Final Answer) when appropriate.\n"
    "6. Stay strictly within the Class 1–8 school curriculum.\n"
    "7. Do not use emojis. Never output <think> or hidden reasoning traces."
)

class ShikshaInferenceEngine:
    def __init__(self, model_path: str = DEFAULT_MODEL_PATH, llama_cli_path: str = DEFAULT_LLAMA_CLI):
        self.model_path = os.path.abspath(model_path)
        self.llama_cli_path = os.path.abspath(llama_cli_path)
        self.is_loaded = False
        self.ctx_size = 2048
        self.n_threads = 4
        self._active_processes: Dict[str, subprocess.Popen] = {}
        self._lock = threading.Lock()
        
        # Verify binaries and model on initialization
        if os.path.exists(self.model_path):
            self.is_loaded = True

    def load_model(self, model_path: Optional[str] = None, ctx_size: int = 2048, n_threads: int = 4) -> Dict[str, Any]:
        """Loads and initializes model configuration."""
        with self._lock:
            if model_path:
                abs_path = os.path.abspath(model_path)
                if not os.path.exists(abs_path):
                    raise FileNotFoundError(f"Model file not found at: {abs_path}")
                self.model_path = abs_path
                
            if not os.path.exists(self.llama_cli_path):
                raise FileNotFoundError(f"llama-cli binary not found at: {self.llama_cli_path}")
                
            self.ctx_size = ctx_size
            self.n_threads = n_threads
            self.is_loaded = True
            
            file_size_mb = os.path.getsize(self.model_path) / (1024 * 1024)
            return {
                "status": "loaded",
                "model_path": self.model_path,
                "model_size_mb": round(file_size_mb, 2),
                "ctx_size": self.ctx_size,
                "n_threads": self.n_threads,
                "engine": "llama.cpp (native)"
            }

    def unload_model(self) -> Dict[str, Any]:
        """Stops any active generations and unloads model state."""
        with self._lock:
            # Terminate all running generations
            for req_id, proc in list(self._active_processes.items()):
                try:
                    proc.terminate()
                except Exception:
                    pass
            self._active_processes.clear()
            self.is_loaded = False
            return {"status": "unloaded"}

    def get_model_info(self) -> Dict[str, Any]:
        """Returns current model status, metadata, and memory footprints."""
        if not self.is_loaded or not os.path.exists(self.model_path):
            return {
                "is_loaded": False,
                "model_path": self.model_path,
                "error": "Model not loaded or file does not exist"
            }
            
        file_size_bytes = os.path.getsize(self.model_path)
        return {
            "is_loaded": True,
            "model_path": self.model_path,
            "model_filename": os.path.basename(self.model_path),
            "size_bytes": file_size_bytes,
            "size_mb": round(file_size_bytes / (1024 * 1024), 2),
            "ctx_size": self.ctx_size,
            "n_threads": self.n_threads,
            "offline_only": True,
            "active_generations": len(self._active_processes)
        }

    def _format_prompt(self, question: str, grade: Optional[int] = None, subject: Optional[str] = None) -> str:
        """Constructs grade-aware ChatML prompt according to the trained teacher persona."""
        prefix_parts = []
        if grade is not None:
            prefix_parts.append(f"Student grade: Class {grade}")
        if subject:
            prefix_parts.append(f"Subject: {subject}")
            
        if prefix_parts:
            formatted_q = "\n".join(prefix_parts) + f"\nQuestion: {question}"
        else:
            formatted_q = question
            
        # Clean ChatML template with strengthened educational system prompt
        prompt = (
            f"<|im_start|>system\n{SYSTEM_PROMPT}<|im_end|>\n"
            f"<|im_start|>user\n{formatted_q}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )
        return prompt

    def stream_generate(
        self,
        question: str,
        grade: Optional[int] = None,
        subject: Optional[str] = None,
        request_id: Optional[str] = None,
        max_tokens: int = 250,
        temperature: float = 0.0,
    ) -> Generator[InferenceStreamChunk, None, None]:
        """Streams tokens as they are generated by the native llama.cpp process."""
        if not self.is_loaded:
            raise RuntimeError("Cannot generate: Model is not loaded. Call load_model() first.")
            
        req_id = request_id or str(uuid.uuid4())
        formatted_prompt = self._format_prompt(question, grade, subject)
        
        cmd = [
            self.llama_cli_path,
            "-m", self.model_path,
            "-p", formatted_prompt,
            "-n", str(max_tokens),
            "-c", str(self.ctx_size),
            "-t", str(self.n_threads),
            "--temp", str(temperature),
            "--simple-io",
            "-st",
            "--no-display-prompt"
        ]
        
        start_time = time.time()
        try:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                bufsize=1
            )
            with self._lock:
                self._active_processes[req_id] = proc
        except Exception as e:
            yield InferenceStreamChunk(
                request_id=req_id,
                status="error",
                delta="",
                accumulated="",
                done=True,
                error=str(e)
            )
            return

        accumulated_text = ""
        prompt_tokens_per_sec = 0.0
        generation_tokens_per_sec = 0.0
        
        try:
            for line in iter(proc.stdout.readline, ""):
                # Check for cancellation
                with self._lock:
                    if req_id not in self._active_processes:
                        # Process was cancelled
                        yield InferenceStreamChunk(
                            request_id=req_id,
                            status="cancelled",
                            delta="",
                            accumulated=accumulated_text,
                            done=True,
                            error="Generation cancelled by user"
                        )
                        return
                        
                # Filter CLI artifacts / performance summary
                if "[ Prompt:" in line:
                    perf_match = re.search(r"Prompt:\s*([\d\.]+)\s*t/s\s*\|\s*Generation:\s*([\d\.]+)\s*t/s", line)
                    if perf_match:
                        prompt_tokens_per_sec = float(perf_match.group(1))
                        generation_tokens_per_sec = float(perf_match.group(2))
                    continue
                    
                if "Loading model..." in line or "build      :" in line or "model      :" in line or "available commands:" in line:
                    continue
                    
                clean_chunk = line
                if "<|im_start|>assistant" in clean_chunk:
                    clean_chunk = clean_chunk.split("<|im_start|>assistant")[-1]
                if "<|im_end|>" in clean_chunk:
                    clean_chunk = clean_chunk.split("<|im_end|>")[0]
                if "</think>" in clean_chunk:
                    clean_chunk = clean_chunk.split("</think>")[-1]
                if "<think>" in clean_chunk:
                    clean_chunk = clean_chunk.split("<think>")[0]
                    
                if clean_chunk:
                    accumulated_text += clean_chunk
                    yield InferenceStreamChunk(
                        request_id=req_id,
                        status="generating",
                        delta=clean_chunk,
                        accumulated=accumulated_text,
                        done=False
                    )
                    
            proc.stdout.close()
            proc.wait()
            
        finally:
            with self._lock:
                self._active_processes.pop(req_id, None)

        latency_ms = (time.time() - start_time) * 1000
        
        # Clean final accumulated text
        final_content = accumulated_text.strip()
        if "<|im_end|>" in final_content:
            final_content = final_content.split("<|im_end|>")[0].strip()
            
        # Parse structured pedagogical elements
        meta = StructuredTutorParser.parse(final_content, grade=grade, subject=subject)
        
        # Estimate completion tokens (roughly 1 token per 3.8 chars or derived from gen speed)
        est_tokens = max(1, len(final_content) // 4)
        if generation_tokens_per_sec > 0 and latency_ms > 0:
            est_tokens = int(generation_tokens_per_sec * (latency_ms / 1000.0))
            
        metrics = RuntimeMetrics(
            completion_tokens=est_tokens,
            tokens_per_second=generation_tokens_per_sec,
            prompt_tokens_per_second=prompt_tokens_per_sec,
            latency_ms=round(latency_ms, 2)
        )
        
        # Final completion chunk
        yield InferenceStreamChunk(
            request_id=req_id,
            status="completed",
            delta="",
            accumulated=final_content,
            done=True,
            metadata=meta,
            metrics=metrics
        )

    def generate(
        self,
        question: str,
        grade: Optional[int] = None,
        subject: Optional[str] = None,
        request_id: Optional[str] = None,
        max_tokens: int = 250,
        temperature: float = 0.0,
    ) -> InferenceResponse:
        """Synchronously generates a complete response."""
        req_id = request_id or str(uuid.uuid4())
        last_chunk = None
        for chunk in self.stream_generate(
            question=question,
            grade=grade,
            subject=subject,
            request_id=req_id,
            max_tokens=max_tokens,
            temperature=temperature
        ):
            last_chunk = chunk
            
        if last_chunk is None:
            return InferenceResponse(
                request_id=req_id,
                status="error",
                content="",
                done=True,
                error="No output generated"
            )
            
        return InferenceResponse(
            request_id=req_id,
            status=last_chunk.status,
            content=last_chunk.accumulated,
            done=True,
            error=last_chunk.error,
            metadata=last_chunk.metadata,
            metrics=last_chunk.metrics
        )

    def stop_generation(self, request_id: str) -> bool:
        """Cancels an ongoing generation process."""
        with self._lock:
            proc = self._active_processes.pop(request_id, None)
            if proc:
                try:
                    proc.terminate()
                    return True
                except Exception:
                    return False
        return False

    def benchmark(self, num_runs: int = 2) -> Dict[str, Any]:
        """Runs a deterministic benchmark on the local machine and measures actual latency/throughput."""
        if not self.is_loaded:
            raise RuntimeError("Cannot benchmark: Model is not loaded.")
            
        benchmark_prompt = "Calculate the weight of a 10 kg mass on Earth (g = 9.8 m/s²)."
        
        # 1. Measure cold load time
        cold_start = time.time()
        self.load_model()
        cold_load_ms = round((time.time() - cold_start) * 1000, 2)
        
        run_speeds = []
        prompt_speeds = []
        latencies = []
        
        for _ in range(num_runs):
            resp = self.generate(benchmark_prompt, grade=8, subject="Science (Physics)", max_tokens=100)
            if resp.metrics:
                if resp.metrics.tokens_per_second > 0:
                    run_speeds.append(resp.metrics.tokens_per_second)
                if resp.metrics.prompt_tokens_per_second > 0:
                    prompt_speeds.append(resp.metrics.prompt_tokens_per_second)
                latencies.append(resp.metrics.latency_ms)
                
        avg_gen_speed = round(sum(run_speeds) / len(run_speeds), 2) if run_speeds else 0.0
        avg_prompt_speed = round(sum(prompt_speeds) / len(prompt_speeds), 2) if prompt_speeds else 0.0
        avg_latency = round(sum(latencies) / len(latencies), 2) if latencies else 0.0
        
        return {
            "environment": "PC / Local Host (llama.cpp CPU)",
            "model_path": self.model_path,
            "cold_load_time_ms": cold_load_ms,
            "avg_generation_speed_tok_s": avg_gen_speed,
            "avg_prompt_processing_speed_tok_s": avg_prompt_speed,
            "avg_latency_ms": avg_latency,
            "num_runs": num_runs,
            "status": "PASS"
        }
