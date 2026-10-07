class HistoryItem {
  final String id;
  final String question;
  final String answer;
  final int grade;
  final String subject;
  final DateTime timestamp;

  HistoryItem({
    required this.id,
    required this.question,
    required this.answer,
    required this.grade,
    required this.subject,
    required this.timestamp,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'question': question,
      'answer': answer,
      'grade': grade,
      'subject': subject,
      'timestamp': timestamp.toIso8601String(),
    };
  }

  factory HistoryItem.fromMap(Map<String, dynamic> map) {
    return HistoryItem(
      id: map['id'] as String,
      question: map['question'] as String,
      answer: map['answer'] as String,
      grade: map['grade'] as int,
      subject: map['subject'] as String,
      timestamp: DateTime.parse(map['timestamp'] as String),
    );
  }
}
