"""
tests/test_backend_service.py
Comprehensive automated test suite for SHIKSHA Inference Backend.
Verifies:
1. Model loading / unloading
2. Synchronous generation
3. Streaming chunk generation
4. Cancellation of active generation
5. Malformed request handling
6. Missing model file handling
7. Runtime metrics extraction
8. Offline integrity (zero external network connections)
9. Tutor pedagogical response quality
"""

import os
import sys
import time
import unittest
import socket

sys.path.insert(0, r"C:\Rounak\RVSHACK")

from backend.inference_engine import ShikshaInferenceEngine
from backend.response_contract import StructuredTutorParser

MODEL_Q4 = r"C:\Rounak\RVSHACK\output\qwen3_k8_tutor_q4_k_m.gguf"

class TestShikshaBackend(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = ShikshaInferenceEngine(model_path=MODEL_Q4)

    def test_01_model_loading(self):
        """Test model load and info inspection."""
        info = self.engine.get_model_info()
        self.assertTrue(info["is_loaded"])
        self.assertEqual(info["model_filename"], "qwen3_k8_tutor_q4_k_m.gguf")
        self.assertTrue(info["size_mb"] > 300)
        self.assertTrue(info["offline_only"])

    def test_02_generation_sync(self):
        """Test synchronous generation returns valid structured response."""
        resp = self.engine.generate(
            question="Solve 3x + 5 = 20 step-by-step.",
            grade=6,
            subject="Mathematics",
            max_tokens=100
        )
        self.assertEqual(resp.status, "completed")
        self.assertTrue(resp.done)
        self.assertIn("5", resp.content)
        self.assertIsNotNone(resp.metrics)
        self.assertTrue(resp.metrics.tokens_per_second > 0)
        self.assertFalse("<think>" in resp.content)

    def test_03_streaming(self):
        """Test token streaming chunk delivery."""
        chunks = []
        for chunk in self.engine.stream_generate(
            question="Calculate 7 × 4.",
            grade=3,
            subject="Mathematics",
            max_tokens=60
        ):
            chunks.append(chunk)
            
        self.assertTrue(len(chunks) > 1, "Expected multiple streaming chunks")
        final_chunk = chunks[-1]
        self.assertTrue(final_chunk.done)
        self.assertEqual(final_chunk.status, "completed")
        self.assertIn("28", final_chunk.accumulated)

    def test_04_cancellation(self):
        """Test cancelling an in-flight generation request."""
        req_id = "test-cancel-123"
        
        # Start generation in a separate generator and cancel after first chunk
        gen = self.engine.stream_generate(
            question="Explain Newton's second law in extensive detail.",
            grade=8,
            subject="Science (Physics)",
            request_id=req_id,
            max_tokens=200
        )
        
        first_chunk = next(gen)
        self.assertFalse(first_chunk.done)
        
        # Trigger cancellation
        cancelled = self.engine.stop_generation(req_id)
        self.assertTrue(cancelled)
        
        # Remaining iterations should yield cancelled status
        final_chunk = None
        for chunk in gen:
            final_chunk = chunk
            
        self.assertIsNotNone(final_chunk)
        self.assertEqual(final_chunk.status, "cancelled")
        self.assertTrue(final_chunk.done)

    def test_05_malformed_request(self):
        """Test handling of empty/malformed inputs."""
        # Generating with empty prompt should still execute or gracefully handle without crash
        resp = self.engine.generate(question="", max_tokens=10)
        self.assertIsNotNone(resp)

    def test_06_missing_model_handling(self):
        """Test error when loading a non-existent model file."""
        fake_engine = ShikshaInferenceEngine(model_path=r"C:\non_existent_model.gguf")
        fake_engine.is_loaded = False
        with self.assertRaises(FileNotFoundError):
            fake_engine.load_model(r"C:\non_existent_model.gguf")

    def test_07_metrics_extraction(self):
        """Test that prompt eval and generation speeds are measurable and non-zero."""
        resp = self.engine.generate(
            question="Calculate 10% of 50.",
            grade=5,
            subject="Mathematics",
            max_tokens=50
        )
        self.assertIsNotNone(resp.metrics)
        self.assertTrue(resp.metrics.latency_ms > 0)
        self.assertTrue(resp.metrics.completion_tokens > 0)

    def test_08_offline_integrity(self):
        """Verify zero external socket connections are initiated during generation."""
        # Monkeypatch socket.create_connection to assert no WAN connections
        orig_connect = socket.socket.connect
        
        def safe_connect(sock, address):
            host, port = address
            if host not in ["127.0.0.1", "localhost", "::1"]:
                raise ConnectionRefusedError(f"EXTERNAL NETWORK BLOCKED: Attempted connection to {host}:{port}")
            return orig_connect(sock, address)
            
        socket.socket.connect = safe_connect
        try:
            resp = self.engine.generate("What is 2 + 2?", grade=1, subject="Mathematics", max_tokens=30)
            self.assertEqual(resp.status, "completed")
            self.assertIn("4", resp.content)
        finally:
            socket.socket.connect = orig_connect

    def test_09_tutor_quality_regression(self):
        """Verify pedagogical structure parser on educational content."""
        sample_output = (
            "Given:\n"
            "3x + 5 = 20\n\n"
            "Required:\n"
            "Value of variable x\n\n"
            "Calculation:\n"
            "Step 1: Subtract 5: 3x = 15\n"
            "Step 2: Divide by 3: x = 5\n\n"
            "Verification:\n"
            "LHS = 20 = RHS\n\n"
            "Final Answer:\n"
            "5"
        )
        meta = StructuredTutorParser.parse(sample_output, grade=6, subject="Mathematics")
        self.assertEqual(meta.answer_type, "numerical_step_by_step")
        self.assertEqual(meta.given, "3x + 5 = 20")
        self.assertEqual(meta.final_answer, "5")
        self.assertTrue(len(meta.steps) >= 2)

if __name__ == "__main__":
    unittest.main()
