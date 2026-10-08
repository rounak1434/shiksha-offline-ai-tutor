import '../models/tutor_message.dart';

class ResponseParser {
  /// Cleans raw LaTeX math delimiters and converts formulas to clean readable plain text
  static String cleanMath(String input) {
    if (input.isEmpty) return input;
    var s = input;

    // Convert \frac{a}{b} to (a) / (b) or a / b
    s = s.replaceAllMapped(
      RegExp(r'\\frac\{([^{}]+)\}\{([^{}]+)\}'),
      (m) => '(${m[1]}) / (${m[2]})',
    );
    // In case of any secondary / nested \frac
    s = s.replaceAllMapped(
      RegExp(r'\\frac\{([^{}]+)\}\{([^{}]+)\}'),
      (m) => '(${m[1]}) / (${m[2]})',
    );

    // Replace \text{...} or \mathrm{...} with its inner content
    s = s.replaceAllMapped(RegExp(r'\\(?:text|mathrm|mathbf)\{([^{}]+)\}'), (m) => m[1] ?? '');
    s = s.replaceAllMapped(RegExp(r'\\(?:text|mathrm|mathbf)\{([^{}]+)\}'), (m) => m[1] ?? '');

    // Replace ^2 and ^3 with unicode superscripts
    s = s.replaceAll('^2', '²');
    s = s.replaceAll('^{2}', '²');
    s = s.replaceAll('^3', '³');
    s = s.replaceAll('^{3}', '³');

    // Common LaTeX symbols
    s = s.replaceAll(r'\times', '*');
    s = s.replaceAll(r'\cdot', '*');
    s = s.replaceAll(r'\div', '/');
    s = s.replaceAll(r'\approx', '≈');
    s = s.replaceAll(r'\pm', '±');
    s = s.replaceAll(r'\le', '<=');
    s = s.replaceAll(r'\ge', '>=');
    s = s.replaceAll(r'\neq', '!=');

    // LaTeX spacing commands
    s = s.replaceAll(r'\,', ' ');
    s = s.replaceAll(r'\;', ' ');
    s = s.replaceAll(r'\quad', ' ');

    // Strip LaTeX dollar signs
    s = s.replaceAll(r'$$', '');
    s = s.replaceAll(r'$', '');

    // Clean any remaining markdown bold markers from section content lines
    s = s.replaceAll(r'**', '');

    return s.trim();
  }

  /// Parses the raw educational response into structured sections matching Stitch design
  static StructuredResponse parse(String text) {
    if (text.trim().isEmpty) {
      return StructuredResponse(rawContent: text);
    }

    String? definition;
    String? explanation;
    String? keyPrinciple;
    String? example;
    String? summary;

    String? given;
    String? required;
    String? formula;
    String? rearrangement;
    String? substitution;
    String? calculation;
    String? unit;
    String? finalAnswer;

    final lines = text.split('\n');
    String currentSection = '';
    StringBuffer currentBuffer = StringBuffer();

    void commitCurrentSection() {
      final raw = currentBuffer.toString().trim();
      if (raw.isEmpty && currentSection.isEmpty) return;
      final content = cleanMath(raw);
      if (content.isEmpty) return;

      switch (currentSection.toLowerCase()) {
        case 'definition':
        case 'concept':
          definition = content;
          break;
        case 'explanation':
          explanation = content;
          break;
        case 'key principle':
        case 'principle':
          keyPrinciple = content;
          break;
        case 'example':
        case 'example/application':
        case 'application':
          example = content;
          break;
        case 'summary':
          summary = content;
          break;
        case 'given':
          given = content;
          break;
        case 'required':
          required = content;
          break;
        case 'formula':
          formula = content;
          break;
        case 'rearrangement':
          rearrangement = content;
          break;
        case 'substitution':
          substitution = content;
          break;
        case 'calculation':
        case 'steps':
          calculation = content;
          break;
        case 'unit':
          unit = content;
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
      if (trimmed.isEmpty) continue;

      // Remove leading bullet/numbering e.g. "- ", "* ", "1. ", "1) "
      var normalized = trimmed.replaceFirst(RegExp(r'^(?:[-*•]|\d+[\.)])\s*'), '');
      // Strip markdown formatting symbols like **, *, _, #
      normalized = normalized.replaceAll(RegExp(r'[*_#]'), '').trim();
      final lower = normalized.toLowerCase();

      String extractRest() {
        final idx = normalized.indexOf(':');
        if (idx != -1 && idx < normalized.length - 1) {
          return normalized.substring(idx + 1).trim();
        }
        return '';
      }

      if (lower.startsWith('definition:') || lower == 'definition') {
        commitCurrentSection();
        currentSection = 'definition';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else if (lower.startsWith('key principle:') ||
          lower == 'key principle' ||
          lower.startsWith('principle:') ||
          lower == 'principle') {
        commitCurrentSection();
        currentSection = 'key principle';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else if (lower.startsWith('given:') || lower == 'given') {
        commitCurrentSection();
        currentSection = 'given';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else if (lower.startsWith('required:') || lower == 'required') {
        commitCurrentSection();
        currentSection = 'required';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else if (lower.startsWith('formula:') || lower == 'formula') {
        commitCurrentSection();
        currentSection = 'formula';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else if (lower.startsWith('rearrangement:') || lower == 'rearrangement') {
        commitCurrentSection();
        currentSection = 'rearrangement';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else if (lower.startsWith('substitution:') || lower == 'substitution') {
        commitCurrentSection();
        currentSection = 'substitution';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else if (lower.startsWith('calculation:') || lower == 'calculation') {
        commitCurrentSection();
        currentSection = 'calculation';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else if (lower.startsWith('unit:') || lower == 'unit') {
        commitCurrentSection();
        currentSection = 'unit';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else if (lower.startsWith('explanation:') || lower == 'explanation') {
        commitCurrentSection();
        currentSection = 'explanation';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else if (lower.startsWith('example/application:') ||
          lower.startsWith('example:') ||
          lower == 'example') {
        commitCurrentSection();
        currentSection = 'example';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else if (lower.startsWith('summary:') || lower == 'summary') {
        commitCurrentSection();
        currentSection = 'summary';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else if (lower.startsWith('final answer:') ||
          lower.startsWith('answer:') ||
          lower == 'final answer') {
        commitCurrentSection();
        currentSection = 'final answer';
        final rest = extractRest();
        if (rest.isNotEmpty) currentBuffer.writeln(rest);
      } else {
        if (currentSection.isNotEmpty) {
          currentBuffer.writeln(line);
        }
      }
    }

    commitCurrentSection();

    return StructuredResponse(
      definition: definition,
      explanation: explanation,
      keyPrinciple: keyPrinciple,
      example: example,
      summary: summary,
      given: given,
      required: required,
      formula: formula,
      rearrangement: rearrangement,
      substitution: substitution,
      calculation: calculation,
      unit: unit,
      finalAnswer: finalAnswer,
      rawContent: text,
    );
  }
}
