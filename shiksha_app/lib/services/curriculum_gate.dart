enum GateStatus {
  match,
  subjectMismatch,
  outOfScope,
  uncertain,
}

class GateEvaluation {
  final GateStatus status;
  final String? detectedSubject;
  final String? message;

  const GateEvaluation({
    required this.status,
    this.detectedSubject,
    this.message,
  });
}

class CurriculumGate {
  /// Evaluates whether a question matches the student's selected class and subject.
  static GateEvaluation evaluate({
    required String question,
    required int grade,
    required String selectedSubject,
  }) {
    final q = question.trim().toLowerCase();
    final sub = selectedSubject.trim();

    // 1. OUT_OF_SCOPE: Check for topics clearly beyond Class 1-8 school curriculum
    if (_isOutOfScope(q)) {
      return GateEvaluation(
        status: GateStatus.outOfScope,
        message:
            "This topic is outside the Class $grade curriculum. In Class $grade $sub, instruction is focused on foundational school curriculum topics. Please ask a question related to your class syllabus.",
      );
    }

    // 2. DETECT DOMINANT SUBJECT
    final detected = _detectSubject(q);

    if (detected == null) {
      // Uncertain / broad question -> allow question to reach LLM with authoritative prompt
      return const GateEvaluation(status: GateStatus.uncertain);
    }

    // 3. CHECK SUBJECT COMPATIBILITY
    if (_isCompatible(detected, sub)) {
      return GateEvaluation(
        status: GateStatus.match,
        detectedSubject: detected,
      );
    }

    // 4. SUBJECT MISMATCH
    final suggestedSubject = _formatSuggestedSubject(detected, sub);
    return GateEvaluation(
      status: GateStatus.subjectMismatch,
      detectedSubject: detected,
      message:
          "This question belongs to $suggestedSubject, but your current subject is $sub. Please switch to $suggestedSubject to continue.",
    );
  }

  static bool _isOutOfScope(String q) {
    const outOfScopePatterns = [
      'quantum field theory',
      'quantum electrodynamics',
      'quantum chromodynamics',
      'string theory',
      'general relativity',
      'tensor calculus',
      'schrodinger equation',
      'schrödinger equation',
      'lagrangian mechanics',
      'hamiltonian mechanics',
      'feynman diagram',
      'higgs boson mechanism',
      'differential equation',
      'differential equations',
      'multivariable calculus',
      'vector calculus',
      'real analysis',
      'abstract algebra',
      'group theory',
      'sn1 reaction',
      'sn2 reaction',
      'reaction mechanism',
      'stereochemistry',
      'nmr spectroscopy',
      'crispr',
      'recombinant dna',
    ];

    for (final pattern in outOfScopePatterns) {
      if (q.contains(pattern)) return true;
    }

    // Check for advanced differential equations like y'' + 4y
    if (RegExp(r"y\s*''\s*\+\s*").hasMatch(q) || RegExp(r"d\^?2y\/d[tx]\^?2").hasMatch(q)) {
      return true;
    }

    return false;
  }

  static String? _detectSubject(String q) {
    // A. Mathematics check
    // Algebra / Equations / Arithmetic formulas
    final hasMathSymbols = RegExp(r'[0-9]+\s*[\+\-\*\/]\s*[0-9]+').hasMatch(q) ||
        RegExp(r'solve\s+[0-9a-z\s\+\-\*\/\=]+=[0-9a-z\s\+\-\*\/]+').hasMatch(q) ||
        RegExp(r'\b[0-9]*[a-z]\s*[\+\-\*\/]\s*[0-9]+\s*=').hasMatch(q) ||
        q.contains('solve 2x') ||
        q.contains('2x +') ||
        q.contains('2x -') ||
        q.contains('3x +') ||
        q.contains('linear equation') ||
        q.contains('quadratic equation') ||
        q.contains('pythagoras theorem') ||
        q.contains('pythagorean theorem') ||
        q.contains('hcf and lcm') ||
        q.contains('prime factorization') ||
        q.contains('simple interest') ||
        q.contains('compound interest') ||
        q.contains('profit and loss') ||
        q.contains('fraction') ||
        q.contains('fractions') ||
        q.contains('trigonometry') ||
        RegExp(r'^\s*a\s*\+\s*b\s*=\s*\??\s*$').hasMatch(q);

    // Make sure questions like "speed = distance / time" aren't confused as pure math
    final hasPhysicsContext = q.contains('speed') ||
        q.contains('velocity') ||
        q.contains('acceleration') ||
        q.contains('force') ||
        q.contains('newton') ||
        q.contains('friction') ||
        q.contains('gravity') ||
        q.contains('density');

    if (hasMathSymbols && !hasPhysicsContext) {
      return 'Mathematics';
    }

    // B. Biology check
    if (q.contains('photosynthesis') ||
        q.contains('chlorophyll') ||
        q.contains('stomata') ||
        q.contains('chloroplast') ||
        q.contains('human bone') ||
        q.contains('human bones') ||
        q.contains('bones does a human') ||
        q.contains('teeth human have') ||
        q.contains('skeleton') ||
        q.contains('digestive system') ||
        q.contains('digestion') ||
        q.contains('respiratory system') ||
        q.contains('respiration') ||
        q.contains('circulatory system') ||
        q.contains('red blood cells') ||
        q.contains('white blood cells') ||
        q.contains('cell membrane') ||
        q.contains('cell wall') ||
        q.contains('mitochondria') ||
        q.contains('pollination') ||
        q.contains('germination') ||
        q.contains('xylem') ||
        q.contains('phloem') ||
        q.contains('ecosystem') ||
        q.contains('food chain') ||
        q.contains('amoeba')) {
      return 'Biology';
    }

    // C. Physics check
    if (q.contains("newton's") ||
        q.contains("newton third") ||
        q.contains("newton's third") ||
        q.contains("newton's second") ||
        q.contains("newton's first") ||
        q.contains("laws of motion") ||
        q.contains("law of motion") ||
        q.contains("f = ma") ||
        q.contains("inertia") ||
        q.contains("friction") ||
        q.contains("mass vs weight") ||
        q.contains("difference between mass and weight") ||
        q.contains("weight on moon") ||
        q.contains("electric current") ||
        q.contains("electric circuit") ||
        q.contains("reflection of light") ||
        q.contains("refraction") ||
        q.contains("concave mirror") ||
        q.contains("convex mirror") ||
        q.contains("sound waves") ||
        q.contains("atmospheric pressure") ||
        q.contains("kinetic energy") ||
        q.contains("potential energy") ||
        q.contains("archimedes principle")) {
      return 'Physics';
    }

    // D. Chemistry check
    if (q.contains('chemical reaction') ||
        q.contains('chemical equation') ||
        q.contains('acids and bases') ||
        q.contains('hydrochloric acid') ||
        q.contains('sulfuric acid') ||
        q.contains('litmus paper') ||
        q.contains('ph scale') ||
        q.contains('neutralization') ||
        q.contains('rusting of iron') ||
        q.contains('reactivity series') ||
        q.contains('atomic number') ||
        q.contains('periodic table') ||
        q.contains('valency') ||
        q.contains('calorific value')) {
      return 'Chemistry';
    }

    // E. Computer Science check
    if (q.contains('python') ||
        q.contains('algorithm') ||
        q.contains('flowchart') ||
        q.contains('binary number') ||
        q.contains('cpu') ||
        q.contains('ram and rom') ||
        q.contains('operating system') ||
        q.contains('programming language') ||
        q.contains('cyber security')) {
      return 'Computer Science';
    }

    return null;
  }

  static bool _isCompatible(String detected, String selected) {
    if (detected == selected) return true;

    // "Science" in K-8 encompasses Biology, Physics, and Chemistry
    if (selected == 'Science') {
      return detected == 'Biology' || detected == 'Physics' || detected == 'Chemistry';
    }

    return false;
  }

  static String _formatSuggestedSubject(String detected, String current) {
    // If user is on a specific science subject (Physics/Chemistry/Biology) or Mathematics
    return detected;
  }
}
