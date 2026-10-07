import 'dart:async';
import 'package:flutter/services.dart';
import 'curriculum_gate.dart';

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
        'model': 'qwen3_base_q4_k_m.gguf',
        'format': 'GGUF Q4_K_M',
        'size_mb': 461.79,
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
    final effectiveGrade = grade ?? 6;
    final effectiveSubject = (subject != null && subject.trim().isNotEmpty) ? subject.trim() : 'Science';

    // 1. Lightweight local curriculum gate check before calling native LLM
    final gate = CurriculumGate.evaluate(
      question: question,
      grade: effectiveGrade,
      selectedSubject: effectiveSubject,
    );

    if (gate.status == GateStatus.subjectMismatch || gate.status == GateStatus.outOfScope) {
      final controller = StreamController<InferenceChunk>();
      final boundaryText = gate.message ?? 'This question is outside the selected subject curriculum.';
      scheduleMicrotask(() {
        controller.add(InferenceChunk(
          status: 'completed',
          delta: boundaryText,
          accumulated: boundaryText,
          done: true,
        ));
        controller.close();
      });
      return controller.stream;
    }

    final isMathOrNumerical = effectiveSubject.toLowerCase().contains('math') ||
        (effectiveSubject.toLowerCase().contains('physics') &&
            (question.contains('calculate') || question.contains('find') || RegExp(r'\d+').hasMatch(question)));

    final structureInstruction = isMathOrNumerical
        ? "For numerical, math, or problem-solving questions, use these structured headings where applicable:\n"
          "Given:\n"
          "Required:\n"
          "Formula:\n"
          "Rearrangement:\n"
          "Substitution:\n"
          "Calculation:\n"
          "Unit:\n"
          "Final Answer:"
        : "For conceptual questions, use these structured headings where applicable:\n"
          "Definition:\n"
          "Explanation:\n"
          "Key Principle:\n"
          "Example/Application:\n"
          "Summary:";

    final controller = StreamController<InferenceChunk>();
    final StringBuffer accumulated = StringBuffer();

    final effectiveMaxTokens = (maxTokens == 250)
        ? _calculateDynamicMaxTokens(question, effectiveSubject)
        : maxTokens;

    final systemPrompt =
        "You are SHIKSHA, an offline school AI tutor for Class 1 to Class 8 students.\n\n"
        "Strict rules:\n"
        "- The student is in Class $effectiveGrade.\n"
        "- The selected subject is authoritative: $effectiveSubject.\n"
        "- Answer only within the selected subject ($effectiveSubject) and Class $effectiveGrade curriculum.\n"
        "- Keep explanations age-appropriate and easy to understand for a Class $effectiveGrade student.\n"
        "- Do not silently switch subjects. Do not answer unrelated questions as if they belong to the selected subject.\n"
        "- If a question belongs to another subject, tell the student to switch to that subject.\n"
        "- If a topic is clearly outside the Class 1–8 school curriculum, politely state that it is outside the school curriculum.\n"
        "- Answer directly and concisely in English. Never output <think> or hidden reasoning tags.\n\n"
        "$structureInstruction";

    final userPrompt =
        "/no_think\n"
        "Student grade: Class $effectiveGrade\n"
        "Subject: $effectiveSubject\n"
        "Question: $question";

    final serializedPrompt =
        "<|im_start|>system\n$systemPrompt<|im_end|>\n"
        "<|im_start|>user\n$userPrompt<|im_end|>\n"
        "<|im_start|>assistant\n";

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
          final rawDelta = event['delta'] as String? ?? '';
          // Avoid leading blank newlines at the start of response
          if (accumulated.isEmpty && rawDelta.trimLeft().isEmpty) {
            return;
          }
          final delta = accumulated.isEmpty ? rawDelta.trimLeft() : rawDelta;
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
