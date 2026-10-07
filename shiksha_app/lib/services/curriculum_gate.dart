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

    // 1. OUT_OF_SCOPE: Check for topics clearly beyond Class 1-8 school curriculum or non-academic
    if (_isOutOfScope(q)) {
      return GateEvaluation(
        status: GateStatus.outOfScope,
        message:
            "SHIKSHA is intended for academic learning for Classes 1–8 within the supported subjects (Mathematics, Science, Computer Science). This topic is outside the school curriculum scope.",
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
      // Advanced physics / collegiate math
      'quantum field theory',
      'quantum electrodynamics',
      'quantum chromodynamics',
      'string theory',
      'general relativity',
      'tensor calculus',
      'schrodinger',
      'schrödinger',
      'lagrangian',
      'hamiltonian',
      'feynman diagram',
      'higgs boson',
      'differential equation',
      'differential equations',
      'multivariable calculus',
      'vector calculus',
      'real analysis',
      'abstract algebra',
      'group theory',
      'linear transformation',
      'eigenvalue',
      'eigenvector',
      'laplace transform',
      'fourier transform',
      // Advanced chemistry & biology
      'sn1',
      'sn2',
      'reaction mechanism',
      'stereochemistry',
      'nmr spectroscopy',
      'crispr',
      'recombinant dna',
      // Non-academic topics
      'cricket match',
      'ipl score',
      'football score',
      'bollywood',
      'hollywood',
      'movie review',
      'video game',
      'minecraft',
      'fortnite',
      'roblox',
      'cryptocurrency',
      'bitcoin',
      'stock market',
      'tell me a joke',
      'write a story about',
    ];

    for (final pattern in outOfScopePatterns) {
      if (q.contains(pattern)) return true;
    }

    // Check for advanced differential equations like y'' + 4y
    if (RegExp(r"y\s*''\s*\+\s*").hasMatch(q) ||
        RegExp(r"d\^?2y\/d[tx]\^?2").hasMatch(q) ||
        RegExp(r"dy\/dx").hasMatch(q)) {
      return true;
    }

    return false;
  }

  static String? _detectSubject(String q) {
    // 1. Computer Science detection
    final isCS = q.contains('python') ||
        q.contains('programming') ||
        q.contains('algorithm') ||
        q.contains('flowchart') ||
        q.contains('binary') ||
        RegExp(r'\b(ram|rom|cpu)\b').hasMatch(q) ||
        q.contains('computer') ||
        q.contains('software') ||
        q.contains('hardware') ||
        q.contains('operating system') ||
        q.contains('input device') ||
        q.contains('output device') ||
        q.contains('storage device') ||
        q.contains('hard disk') ||
        q.contains('ssd') ||
        q.contains('internet') ||
        q.contains('world wide web') ||
        q.contains('cyber') ||
        q.contains('loop in python') ||
        q.contains('variable in python');

    if (isCS) {
      return 'Computer Science';
    }

    // 2. Mathematics detection
    final hasMathExpr = RegExp(r'\d+\s*[\+\-\*\/]\s*\d+').hasMatch(q) ||
        RegExp(r'\b\d+x\b').hasMatch(q) ||
        (q.contains('=') && (q.contains('x') || q.contains('y') || q.contains('a') || q.contains('b'))) ||
        RegExp(r'^\s*a\s*\+\s*b\s*=\s*\??\s*$').hasMatch(q);

    final hasMathKeywords = q.contains('solve') ||
        q.contains('equation') ||
        q.contains('algebra') ||
        q.contains('quadratic') ||
        q.contains('polynomial') ||
        q.contains('fraction') ||
        q.contains('fractions') ||
        q.contains('decimal') ||
        q.contains('percentage') ||
        q.contains('percent') ||
        q.contains('ratio') ||
        q.contains('proportion') ||
        q.contains('pythagor') ||
        q.contains('hypotenuse') ||
        q.contains('perimeter') ||
        q.contains('circumference') ||
        q.contains('area of') ||
        q.contains('volume of') ||
        q.contains('hcf') ||
        q.contains('lcm') ||
        q.contains('prime factor') ||
        q.contains('prime number') ||
        q.contains('square root') ||
        q.contains('cube root') ||
        q.contains('simple interest') ||
        q.contains('compound interest') ||
        q.contains('profit and loss') ||
        q.contains('trigonometry');

    // Make sure physics problems that happen to contain formulas aren't misclassified
    final hasPhysicsContext = q.contains('speed') ||
        q.contains('velocity') ||
        q.contains('acceleration') ||
        q.contains('force') ||
        q.contains('newton') ||
        q.contains('friction') ||
        q.contains('gravity') ||
        q.contains('weight') ||
        q.contains('mass') ||
        q.contains('density') ||
        q.contains('energy') ||
        q.contains('current') ||
        q.contains('voltage') ||
        q.contains('circuit');

    if ((hasMathExpr || hasMathKeywords) && !hasPhysicsContext) {
      return 'Mathematics';
    }

    // 3. Biology detection
    final isBiology = q.contains('photosynthesis') ||
        q.contains('chlorophyll') ||
        q.contains('chloroplast') ||
        q.contains('stomata') ||
        q.contains('bone') ||
        q.contains('bones') ||
        q.contains('skeleton') ||
        q.contains('teeth') ||
        q.contains('tooth') ||
        q.contains('digestive') ||
        q.contains('digestion') ||
        q.contains('stomach') ||
        q.contains('intestine') ||
        q.contains('respiratory') ||
        q.contains('respiration') ||
        q.contains('lungs') ||
        q.contains('circulatory') ||
        q.contains('heart') ||
        q.contains('blood') ||
        q.contains('cell membrane') ||
        q.contains('cell wall') ||
        q.contains('mitochondria') ||
        q.contains('plant cell') ||
        q.contains('animal cell') ||
        q.contains('pollination') ||
        q.contains('germination') ||
        q.contains('xylem') ||
        q.contains('phloem') ||
        q.contains('ecosystem') ||
        q.contains('food chain') ||
        q.contains('food web') ||
        q.contains('herbivore') ||
        q.contains('carnivore') ||
        q.contains('amoeba') ||
        q.contains('bacteria');

    if (isBiology) {
      return 'Biology';
    }

    // 4. Physics detection
    final isPhysics = q.contains("newton") ||
        q.contains("laws of motion") ||
        q.contains("law of motion") ||
        q.contains("f = ma") ||
        q.contains("inertia") ||
        q.contains("friction") ||
        q.contains("gravity") ||
        q.contains("mass vs weight") ||
        q.contains("weight vs mass") ||
        q.contains("weight on moon") ||
        q.contains("speed") ||
        q.contains("velocity") ||
        q.contains("acceleration") ||
        q.contains("work and energy") ||
        q.contains("kinetic energy") ||
        q.contains("potential energy") ||
        q.contains("electric current") ||
        q.contains("circuit") ||
        q.contains("ohm's law") ||
        q.contains("reflection of light") ||
        q.contains("refraction") ||
        q.contains("concave") ||
        q.contains("convex") ||
        q.contains("sound waves") ||
        q.contains("frequency") ||
        q.contains("atmospheric pressure") ||
        q.contains("archimedes principle") ||
        q.contains("density and buoyancy");

    if (isPhysics) {
      return 'Physics';
    }

    // 5. Chemistry detection
    final isChemistry = q.contains('chemical reaction') ||
        q.contains('chemical equation') ||
        q.contains('chemical change') ||
        q.contains('physical vs chemical') ||
        q.contains('acid') ||
        q.contains('base') ||
        q.contains('alkali') ||
        q.contains('ph scale') ||
        q.contains('litmus') ||
        q.contains('neutralization') ||
        q.contains('atom') ||
        q.contains('molecule') ||
        q.contains('elements and compounds') ||
        q.contains('periodic table') ||
        q.contains('valency') ||
        q.contains('rusting') ||
        q.contains('corrosion') ||
        q.contains('combustion') ||
        q.contains('filtration') ||
        q.contains('distillation');

    if (isChemistry) {
      return 'Chemistry';
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
    // If user is on Computer Science or Math and question is Biology/Physics/Chemistry,
    // they can switch to "Science" (or the specific science subject)
    return detected;
  }
}
