import '../models/tutor_message.dart';

class ResponseParser {
  /// Parses the raw educational response into structured sections matching Stitch design
  static StructuredResponse parse(String text) {
    if (text.trim().isEmpty) {
      return StructuredResponse(rawContent: text);
    }

    String? definition;
    String? given;
    String? formula;
    List<String> steps = [];
    String? example;
    String? summary;
    String? finalAnswer;

    final lines = text.split('\n');
    String currentSection = '';
    StringBuffer currentBuffer = StringBuffer();

    void commitCurrentSection() {
      final content = currentBuffer.toString().trim();
      if (content.isEmpty && currentSection.isEmpty) return;

      switch (currentSection.toLowerCase()) {
        case 'definition':
        case 'concept':
          definition = content;
          break;
        case 'given':
          given = content;
          break;
        case 'formula':
          formula = content;
          break;
        case 'explanation':
        case 'steps':
        case 'step-by-step':
          // Split into numbered items if available
          final stepLines = content.split('\n').where((l) => l.trim().isNotEmpty).toList();
          if (stepLines.isNotEmpty) {
            steps = stepLines;
          } else {
            steps = [content];
          }
          break;
        case 'example':
        case 'substitution':
          example = content;
          break;
        case 'summary':
          summary = content;
          break;
        case 'final answer':
        case 'answer':
          finalAnswer = content;
          break;
      }
      currentBuffer.clear();
    }

    for (var line in lines) {
      final trimmed = line.trim();
      final lower = trimmed.toLowerCase();

      if (lower.startsWith('definition:') || lower == 'definition' ||
          lower.startsWith('key principle:') || lower == 'key principle') {
        commitCurrentSection();
        currentSection = 'definition';
        final idx = trimmed.indexOf(':');
        if (idx != -1 && idx < trimmed.length - 1) {
          currentBuffer.writeln(trimmed.substring(idx + 1).trim());
        }
      } else if (lower.startsWith('given:') || lower == 'given' ||
          lower.startsWith('required:') || lower == 'required') {
        commitCurrentSection();
        currentSection = 'given';
        final idx = trimmed.indexOf(':');
        if (idx != -1 && idx < trimmed.length - 1) {
          currentBuffer.writeln(trimmed.substring(idx + 1).trim());
        }
      } else if (lower.startsWith('formula:') || lower == 'formula') {
        commitCurrentSection();
        currentSection = 'formula';
        final idx = trimmed.indexOf(':');
        if (idx != -1 && idx < trimmed.length - 1) {
          currentBuffer.writeln(trimmed.substring(idx + 1).trim());
        }
      } else if (lower.startsWith('explanation:') ||
          lower.startsWith('steps:') ||
          lower.startsWith('calculation:') ||
          lower.startsWith('rearrangement:') ||
          lower == 'explanation' ||
          lower == 'steps' ||
          lower == 'calculation') {
        commitCurrentSection();
        currentSection = 'explanation';
        final idx = trimmed.indexOf(':');
        if (idx != -1 && idx < trimmed.length - 1) {
          final rest = trimmed.substring(idx + 1).trim();
          if (rest.isNotEmpty) currentBuffer.writeln(rest);
        }
      } else if (lower.startsWith('example:') ||
          lower.startsWith('substitution:') ||
          lower.startsWith('example/application:') ||
          lower == 'example') {
        commitCurrentSection();
        currentSection = 'example';
        final idx = trimmed.indexOf(':');
        if (idx != -1 && idx < trimmed.length - 1) {
          currentBuffer.writeln(trimmed.substring(idx + 1).trim());
        }
      } else if (lower.startsWith('summary:') || lower == 'summary') {
        commitCurrentSection();
        currentSection = 'summary';
        final idx = trimmed.indexOf(':');
        if (idx != -1 && idx < trimmed.length - 1) {
          currentBuffer.writeln(trimmed.substring(idx + 1).trim());
        }
      } else if (lower.startsWith('final answer:') ||
          lower.startsWith('answer:') ||
          lower.startsWith('unit:') ||
          lower == 'final answer') {
        commitCurrentSection();
        currentSection = 'final answer';
        final idx = trimmed.indexOf(':');
        if (idx != -1 && idx < trimmed.length - 1) {
          currentBuffer.writeln(trimmed.substring(idx + 1).trim());
        }
      } else {
        if (currentSection.isNotEmpty) {
          currentBuffer.writeln(line);
        }
      }
    }

    commitCurrentSection();

    return StructuredResponse(
      definition: definition,
      given: given,
      formula: formula,
      steps: steps,
      example: example,
      summary: summary,
      finalAnswer: finalAnswer,
      rawContent: text,
    );
  }
}
