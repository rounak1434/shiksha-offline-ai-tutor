import '../services/shiksha_tutor_service.dart';

enum MessageSender { student, tutor }

class StructuredResponse {
  final String? definition;
  final String? explanation;
  final String? keyPrinciple;
  final String? example;
  final String? summary;

  // Numerical / calculation fields
  final String? given;
  final String? required;
  final String? formula;
  final String? rearrangement;
  final String? substitution;
  final String? calculation;
  final String? unit;
  final String? finalAnswer;

  final List<String> steps;
  final String? rawContent;

  StructuredResponse({
    this.definition,
    this.explanation,
    this.keyPrinciple,
    this.example,
    this.summary,
    this.given,
    this.required,
    this.formula,
    this.rearrangement,
    this.substitution,
    this.calculation,
    this.unit,
    this.finalAnswer,
    this.steps = const [],
    this.rawContent,
  });

  bool get hasStructuredSections =>
      definition != null ||
      explanation != null ||
      keyPrinciple != null ||
      example != null ||
      summary != null ||
      given != null ||
      required != null ||
      formula != null ||
      rearrangement != null ||
      substitution != null ||
      calculation != null ||
      unit != null ||
      finalAnswer != null ||
      steps.isNotEmpty;
}

class TutorMessage {
  final String id;
  final MessageSender sender;
  final String content;
  final DateTime timestamp;
  final int grade;
  final String subject;
  final bool isGenerating;
  final String? error;
  final RuntimeMetrics? metrics;
  final StructuredResponse? structuredResponse;

  TutorMessage({
    required this.id,
    required this.sender,
    required this.content,
    required this.timestamp,
    required this.grade,
    required this.subject,
    this.isGenerating = false,
    this.error,
    this.metrics,
    this.structuredResponse,
  });

  TutorMessage copyWith({
    String? content,
    bool? isGenerating,
    String? error,
    RuntimeMetrics? metrics,
    StructuredResponse? structuredResponse,
  }) {
    return TutorMessage(
      id: id,
      sender: sender,
      content: content ?? this.content,
      timestamp: timestamp,
      grade: grade,
      subject: subject,
      isGenerating: isGenerating ?? this.isGenerating,
      error: error ?? this.error,
      metrics: metrics ?? this.metrics,
      structuredResponse: structuredResponse ?? this.structuredResponse,
    );
  }
}
