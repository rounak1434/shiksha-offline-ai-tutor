import '../services/shiksha_tutor_service.dart';

enum MessageSender { student, tutor }

class StructuredResponse {
  final String? definition;
  final String? given;
  final String? formula;
  final List<String> steps;
  final String? example;
  final String? summary;
  final String? finalAnswer;
  final String? rawContent;

  StructuredResponse({
    this.definition,
    this.given,
    this.formula,
    this.steps = const [],
    this.example,
    this.summary,
    this.finalAnswer,
    this.rawContent,
  });

  bool get hasStructuredSections =>
      definition != null ||
      given != null ||
      formula != null ||
      steps.isNotEmpty ||
      example != null ||
      summary != null ||
      finalAnswer != null;
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
