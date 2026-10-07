import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shiksha_app/main.dart';
import 'package:shiksha_app/services/shiksha_tutor_service.dart';
import 'package:shiksha_app/services/response_parser.dart';

class MockTutorService implements IShikshaTutorService {
  @override
  Future<bool> loadModel(String modelPath) async => true;

  @override
  Future<void> unloadModel() async {}

  @override
  Future<void> stopGeneration() async {}

  @override
  Future<Map<String, dynamic>> getModelInfo() async => {
        'engine': 'llama.cpp Mock',
        'format': 'GGUF Q4_K_M',
        'offline': true,
      };

  @override
  Stream<InferenceChunk> streamGenerate({
    required String question,
    int? grade,
    String? subject,
    int maxTokens = 250,
  }) async* {
    yield InferenceChunk(
      status: 'generating',
      delta: 'Definition:\nPhotosynthesis is a process.\n\nSummary:\nProduces glucose.',
      accumulated: 'Definition:\nPhotosynthesis is a process.\n\nSummary:\nProduces glucose.',
      done: true,
      metrics: RuntimeMetrics(
        tokensPerSecond: 14.5,
        promptTokensPerSecond: 137.8,
        completionTokens: 25,
        latencyMs: 150.0,
      ),
    );
  }
}

void main() {
  test('ResponseParser parses structured academic sections correctly', () {
    const raw = '''Definition:
Newton's Second Law states F = ma.

Formula:
F = ma

Explanation:
1. Step one.
2. Step two.

Summary:
Force equals mass times acceleration.''';

    final structured = ResponseParser.parse(raw);
    expect(structured.hasStructuredSections, isTrue);
    expect(structured.definition, contains("Newton's Second Law"));
    expect(structured.formula, contains('F = ma'));
    expect(structured.steps.length, equals(2));
    expect(structured.summary, contains('Force equals mass'));
  });

  testWidgets('ShikshaApp renders Stitch UI with title and grade/subject pills',
      (WidgetTester tester) async {
    final mockService = MockTutorService();
    await tester.pumpWidget(ShikshaApp(tutorService: mockService));
    await tester.pumpAndSettle();

    // Verify Title in RichText
    expect(
      find.byWidgetPredicate(
        (w) => w is RichText && w.text.toPlainText().trim() == 'SHIKSHA',
      ),
      findsOneWidget,
    );

    // Verify Chips
    expect(find.text('Class 6'), findsOneWidget);
    expect(find.text('Science'), findsOneWidget);

    // Verify Input Field
    expect(find.text('Ask your question...'), findsOneWidget);
  });
}
