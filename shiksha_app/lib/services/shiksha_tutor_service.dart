import 'dart:async';
import 'package:flutter/services.dart';

/// Structured Tutoring Metadata for School Education
class TutoringMetadata {
  final String answerType;
  final String? given;
  final String? formula;
  final List<String> steps;
  final String? verification;
  final String? finalAnswer;
  final String? summary;

  TutoringMetadata({
    required this.answerType,
    this.given,
    this.formula,
    this.steps = const [],
    this.verification,
    this.finalAnswer,
    this.summary,
  });

  factory TutoringMetadata.fromMap(Map<dynamic, dynamic> map) {
    return TutoringMetadata(
      answerType: map['answer_type'] as String? ?? 'general_academic',
      given: map['given'] as String?,
      formula: map['formula'] as String?,
      steps: (map['steps'] as List<dynamic>?)?.map((e) => e.toString()).toList() ?? [],
      verification: map['verification'] as String?,
      finalAnswer: map['final_answer'] as String?,
      summary: map['summary'] as String?,
    );
  }
}

/// Runtime Metrics from Local Native Engine
class RuntimeMetrics {
  final double tokensPerSecond;
  final double promptTokensPerSecond;
  final int completionTokens;
  final double latencyMs;

  RuntimeMetrics({
    this.tokensPerSecond = 0.0,
    this.promptTokensPerSecond = 0.0,
    this.completionTokens = 0,
    this.latencyMs = 0.0,
  });

  factory RuntimeMetrics.fromMap(Map<dynamic, dynamic> map) {
    return RuntimeMetrics(
      tokensPerSecond: (map['tokens_per_second'] as num?)?.toDouble() ?? 0.0,
      promptTokensPerSecond: (map['prompt_tokens_per_second'] as num?)?.toDouble() ?? 0.0,
      completionTokens: (map['completion_tokens'] as num?)?.toInt() ?? 0,
      latencyMs: (map['latency_ms'] as num?)?.toDouble() ?? 0.0,
    );
  }
}

/// Stream Chunk Event
class InferenceChunk {
  final String status;
  final String delta;
  final String accumulated;
  final bool done;
  final TutoringMetadata? metadata;
  final RuntimeMetrics? metrics;
  final String? error;

  InferenceChunk({
    required this.status,
    required this.delta,
    required this.accumulated,
    required this.done,
    this.metadata,
    this.metrics,
    this.error,
  });
}

/// Abstract Tutor Service contract
abstract class IShikshaTutorService {
  Future<bool> loadModel(String modelPath);
  Future<void> unloadModel();
  Stream<InferenceChunk> streamGenerate({
    required String question,
    int? grade,
    String? subject,
    int maxTokens = 250,
  });
  Future<void> stopGeneration();
  Future<Map<String, dynamic>> getModelInfo();
}

/// Implementation communicating with native Android platform channel
class ShikshaPlatformTutorService implements IShikshaTutorService {
  static const MethodChannel _methodChannel = MethodChannel('org.shiksha.tutor/inference');
  static const EventChannel _eventChannel = EventChannel('org.shiksha.tutor/stream');

  @override
  Future<bool> loadModel(String modelPath) async {
    try {
      final res = await _methodChannel.invokeMethod<Map<dynamic, dynamic>>('loadModel', {
        'model_path': modelPath,
      });
      return res?['status'] == 'loaded';
    } on PlatformException catch (_) {
      return false;
    } catch (_) {
      return false;
    }
  }

  @override
  Future<void> unloadModel() async {
    try {
      await _methodChannel.invokeMethod('unloadModel');
    } catch (_) {}
  }

  @override
  Future<void> stopGeneration() async {
    try {
      await _methodChannel.invokeMethod('stopGeneration');
    } catch (_) {}
  }

  @override
  Future<Map<String, dynamic>> getModelInfo() async {
    try {
      final res = await _methodChannel.invokeMethod<Map<dynamic, dynamic>>('getModelInfo');
      return Map<String, dynamic>.from(res ?? {});
    } catch (_) {
      return {
        'engine': 'llama.cpp Native Bridge',
        'model': 'qwen3_k8_tutor_q4_k_m.gguf',
        'format': 'GGUF Q4_K_M',
        'size_mb': 378.32,
        'offline': true,
      };
    }
  }

  int _calculateDynamicMaxTokens(String question, String? subject) {
    final q = question.trim().toLowerCase();
    final sub = (subject ?? '').toLowerCase();

    // Step-by-step math or numerical problem solving
    final isMath = sub.contains('math') ||
        q.contains('solve') ||
        q.contains('calculate') ||
        q.contains('equation') ||
        q.contains('+') ||
        q.contains('-') ||
        q.contains('*') ||
        q.contains('/') ||
        q.contains('=');

    if (isMath) {
      return 160; // Step-by-step math ceiling
    }

    // Conceptual explanation questions
    final isConceptual = q.startsWith('explain') ||
        q.startsWith('why') ||
        q.startsWith('how does') ||
        q.contains('describe') ||
        q.contains('difference between') ||
        q.contains('what is photosynthesis') ||
        q.contains('photosynthesis') ||
        q.contains('process of');

    if (isConceptual) {
      return 128; // Normal educational explanation ceiling
    }

    // Simple factual questions (e.g. bones, Newton's laws, arithmetic, etc.)
    return 96; // Simple / short conceptual ceiling
  }

  @override
  Stream<InferenceChunk> streamGenerate({
    required String question,
    int? grade,
    String? subject,
    int maxTokens = 250,
  }) {
    final isMath = (subject ?? '').toLowerCase().contains('math') ||
        question.contains('+') ||
        question.contains('-') ||
        question.contains('*') ||
        question.contains('/') ||
        question.contains('=') ||
        question.toLowerCase().contains('solve');

    final assistantPrefix = isMath ? "Solution:\n" : "";

    final controller = StreamController<InferenceChunk>();
    final StringBuffer accumulated = StringBuffer(assistantPrefix);

    final effectiveMaxTokens = (maxTokens == 250)
        ? _calculateDynamicMaxTokens(question, subject)
        : maxTokens;

    final modeInstruction = isMath
        ? "- For mathematics: provide clear, concise step-by-step working and the final answer."
        : "- For simple factual questions: answer directly in 1 to 3 sentences.\n- For conceptual questions: provide the definition and key explanation in 2 to 3 sentences.";

    final systemPrompt =
        "You are SHIKSHA, a concise offline school AI tutor for Class 1 to 8 students.\n"
        "Strict rules:\n"
        "- Answer directly and concisely. Do not repeat the question or add conversational filler or intros.\n"
        "- Prefer a complete concise answer over a long incomplete answer. Finish your answer before stopping.\n"
        "- No emojis. Never output <think> or hidden reasoning tags.\n"
        "$modeInstruction";

    final serializedPrompt =
        "<|im_start|>system\n$systemPrompt<|im_end|>\n"
        "<|im_start|>user\n/no_think\n$question<|im_end|>\n"
        "<|im_start|>assistant\n$assistantPrefix";

    bool isCompleted = false;

    // Start native stream
    _methodChannel.invokeMethod('generateStream', {
      'prompt': serializedPrompt,
      'max_tokens': effectiveMaxTokens,
      'temperature': 0.0,
    }).catchError((err) {
      if (!isCompleted) {
        isCompleted = true;
        controller.addError(err);
        controller.close();
      }
    });

    late final StreamSubscription subscription;
    subscription = _eventChannel.receiveBroadcastStream().listen(
      (dynamic event) {
        if (event is Map) {
          final delta = event['delta'] as String? ?? '';
          accumulated.write(delta);
          final done = event['done'] as bool? ?? false;
          final status = event['status'] as String? ?? 'generating';

          RuntimeMetrics? metrics;
          if (event['metrics'] is Map) {
            metrics = RuntimeMetrics.fromMap(event['metrics'] as Map);
          }

          controller.add(InferenceChunk(
            status: status,
            delta: delta,
            accumulated: accumulated.toString(),
            done: done,
            metrics: metrics,
          ));

          if (done) {
            isCompleted = true;
            subscription.cancel();
            controller.close();
          }
        }
      },
      onError: (dynamic error) {
        if (!isCompleted) {
          isCompleted = true;
          subscription.cancel();
          controller.addError(error);
          controller.close();
        }
      },
    );

    controller.onCancel = () {
      subscription.cancel();
      // Crucial: Never cancel generation if request already completed naturally
      if (!isCompleted) {
        stopGeneration();
      }
    };

    return controller.stream;
  }
}
