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

  @override
  Stream<InferenceChunk> streamGenerate({
    required String question,
    int? grade,
    String? subject,
    int maxTokens = 250,
  }) {
    final controller = StreamController<InferenceChunk>();
    final StringBuffer accumulated = StringBuffer();

    const systemPrompt =
        "You are SHIKSHA, an offline school AI tutor for Class 1 to 8 students.\n"
        "Follow these instructions strictly:\n"
        "1. Answer the student's actual question directly and accurately.\n"
        "2. Never return generic educational filler or invent missing values.\n"
        "3. If given an algebraic expression with unknown variables where no values are provided, "
        "explicitly state that a numerical answer cannot be calculated without the values of the variables.\n"
        "4. For mathematical calculations, calculate step-by-step when numbers are given.\n"
        "5. Use structured sections (Given, Required, Formula, Explanation, Final Answer) when appropriate.\n"
        "6. Stay strictly within the Class 1–8 school curriculum.\n"
        "7. Do not use emojis. Never output <think> or hidden reasoning traces.";

    final serializedPrompt =
        "<|im_start|>system\n$systemPrompt<|im_end|>\n"
        "<|im_start|>user\nStudent grade: Class $grade\nSubject: $subject\nQuestion: $question<|im_end|>\n"
        "<|im_start|>assistant\n";

    // Start native stream
    _methodChannel.invokeMethod('generateStream', {
      'prompt': serializedPrompt,
      'max_tokens': maxTokens,
      'temperature': 0.0,
    }).catchError((err) {
      controller.addError(err);
      controller.close();
    });

    final subscription = _eventChannel.receiveBroadcastStream().listen(
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
            controller.close();
          }
        }
      },
      onError: (dynamic error) {
        controller.addError(error);
        controller.close();
      },
    );

    controller.onCancel = () {
      subscription.cancel();
      stopGeneration();
    };

    return controller.stream;
  }
}
