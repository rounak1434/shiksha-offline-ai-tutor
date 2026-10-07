import 'dart:async';
import 'package:flutter/material.dart';
import '../models/tutor_message.dart';
import '../models/history_item.dart';
import '../services/shiksha_tutor_service.dart';
import '../services/response_parser.dart';

class ChatScreen extends StatefulWidget {
  final IShikshaTutorService tutorService;

  const ChatScreen({
    super.key,
    required this.tutorService,
  });

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _inputController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  
  int _selectedGrade = 6;
  String _selectedSubject = 'Science';
  bool _isGenerating = false;
  StreamSubscription<InferenceChunk>? _streamSubscription;

  final List<int> _grades = [1, 2, 3, 4, 5, 6, 7, 8];
  final List<String> _subjects = [
    'Science',
    'Mathematics',
    'Physics',
    'Chemistry',
    'Biology',
    'Computer Science'
  ];

  final List<TutorMessage> _messages = [];
  final List<HistoryItem> _history = [];

  @override
  void initState() {
    super.initState();
    // Trigger offline model readiness / load on launch
    widget.tutorService.loadModel('');
    // Default welcome state
    _addInitialGreeting();
  }

  void _addInitialGreeting() {
    _messages.add(
      TutorMessage(
        id: 'msg_welcome',
        sender: MessageSender.tutor,
        content:
            'Definition:\nSHIKSHA is an offline personal AI tutor designed specifically for school students from Class 1 to Class 8.\n\nExplanation:\n1. Choose your grade and subject above.\n2. Ask any academic question or concept problem.\n3. Receive a structured step-by-step verified explanation completely offline.\n\nSummary:\nYour personal offline teacher is ready to help.',
        timestamp: DateTime.now(),
        grade: _selectedGrade,
        subject: _selectedSubject,
        structuredResponse: ResponseParser.parse(
          'Definition:\nSHIKSHA is an offline personal AI tutor designed specifically for school students from Class 1 to Class 8.\n\nExplanation:\n1. Choose your grade and subject above.\n2. Ask any academic question or concept problem.\n3. Receive a structured step-by-step verified explanation completely offline.\n\nSummary:\nYour personal offline teacher is ready to help.',
        ),
      ),
    );
  }

  @override
  void dispose() {
    _streamSubscription?.cancel();
    _inputController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 250),
          curve: Curves.easeOut,
        );
      }
    });
  }

  void _newConversation() {
    if (_isGenerating) {
      _stopGeneration();
    }
    setState(() {
      _messages.clear();
      _addInitialGreeting();
    });
  }

  void _stopGeneration() {
    _streamSubscription?.cancel();
    widget.tutorService.stopGeneration();
    setState(() {
      _isGenerating = false;
      if (_messages.isNotEmpty && _messages.last.sender == MessageSender.tutor) {
        _messages[_messages.length - 1] = _messages.last.copyWith(isGenerating: false);
      }
    });
  }

  void _submitQuestion([String? presetText]) {
    final text = (presetText ?? _inputController.text).trim();
    if (text.isEmpty || _isGenerating) return;

    if (presetText == null) {
      _inputController.clear();
    }

    final studentMsg = TutorMessage(
      id: 'msg_std_${DateTime.now().millisecondsSinceEpoch}',
      sender: MessageSender.student,
      content: text,
      timestamp: DateTime.now(),
      grade: _selectedGrade,
      subject: _selectedSubject,
    );

    final tutorMsgId = 'msg_tut_${DateTime.now().millisecondsSinceEpoch}';
    final tutorMsg = TutorMessage(
      id: tutorMsgId,
      sender: MessageSender.tutor,
      content: '',
      timestamp: DateTime.now(),
      grade: _selectedGrade,
      subject: _selectedSubject,
      isGenerating: true,
    );

    setState(() {
      _messages.add(studentMsg);
      _messages.add(tutorMsg);
      _isGenerating = true;
    });
    _scrollToBottom();

    // Stream generation from native backend
    try {
      _streamSubscription = widget.tutorService
          .streamGenerate(
        question: text,
        grade: _selectedGrade,
        subject: _selectedSubject,
      )
          .listen(
        (chunk) {
          final tutorIndex = _messages.indexWhere((m) => m.id == tutorMsgId);
          if (tutorIndex == -1) return;

          final updatedStructured = ResponseParser.parse(chunk.accumulated);

          setState(() {
            _messages[tutorIndex] = _messages[tutorIndex].copyWith(
              content: chunk.accumulated,
              isGenerating: !chunk.done,
              metrics: chunk.metrics,
              structuredResponse: updatedStructured,
            );
            if (chunk.done) {
              _isGenerating = false;
              // Save to history
              _history.insert(
                0,
                HistoryItem(
                  id: tutorMsgId,
                  question: text,
                  answer: chunk.accumulated,
                  grade: _selectedGrade,
                  subject: _selectedSubject,
                  timestamp: DateTime.now(),
                ),
              );
            }
          });
          _scrollToBottom();
        },
        onError: (error) {
          final tutorIndex = _messages.indexWhere((m) => m.id == tutorMsgId);
          if (tutorIndex != -1) {
            setState(() {
              _messages[tutorIndex] = _messages[tutorIndex].copyWith(
                isGenerating: false,
                error: 'Offline inference service encountered an issue. Please try again.',
              );
              _isGenerating = false;
            });
          }
        },
        onDone: () {
          setState(() {
            _isGenerating = false;
          });
        },
      );
    } catch (e) {
      final tutorIndex = _messages.indexWhere((m) => m.id == tutorMsgId);
      if (tutorIndex != -1) {
        setState(() {
          _messages[tutorIndex] = _messages[tutorIndex].copyWith(
            isGenerating: false,
            error: 'Could not connect to local model. Please verify offline model is loaded.',
          );
          _isGenerating = false;
        });
      }
    }
  }

  void _showGradePicker() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF111C2A),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 16),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text(
                  'Select Grade (Class 1 – 8)',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 12,
                  runSpacing: 12,
                  alignment: WrapAlignment.center,
                  children: _grades.map((g) {
                    final isSelected = g == _selectedGrade;
                    return InkWell(
                      onTap: () {
                        setState(() => _selectedGrade = g);
                        Navigator.pop(context);
                      },
                      borderRadius: BorderRadius.circular(20),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                        decoration: BoxDecoration(
                          color: isSelected ? const Color(0xFF38BDF8) : const Color(0xFF1E293B),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(
                            color: isSelected ? const Color(0xFF38BDF8) : const Color(0xFF334155),
                          ),
                        ),
                        child: Text(
                          'Class $g',
                          style: TextStyle(
                            color: isSelected ? Colors.black : Colors.white,
                            fontWeight: FontWeight.w600,
                            fontSize: 14,
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  void _showSubjectPicker() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF111C2A),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return SafeArea(
          child: Padding(
            padding: const EdgeInsets.symmetric(vertical: 16),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text(
                  'Select Subject',
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                const SizedBox(height: 12),
                Wrap(
                  spacing: 10,
                  runSpacing: 10,
                  alignment: WrapAlignment.center,
                  children: _subjects.map((sub) {
                    final isSelected = sub == _selectedSubject;
                    return InkWell(
                      onTap: () {
                        setState(() => _selectedSubject = sub);
                        Navigator.pop(context);
                      },
                      borderRadius: BorderRadius.circular(20),
                      child: Container(
                        padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 8),
                        decoration: BoxDecoration(
                          color: isSelected ? const Color(0xFF38BDF8) : const Color(0xFF1E293B),
                          borderRadius: BorderRadius.circular(20),
                          border: Border.all(
                            color: isSelected ? const Color(0xFF38BDF8) : const Color(0xFF334155),
                          ),
                        ),
                        child: Text(
                          sub,
                          style: TextStyle(
                            color: isSelected ? Colors.black : Colors.white,
                            fontWeight: FontWeight.w600,
                            fontSize: 13,
                          ),
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  void _showHistoryModal() {
    showModalBottomSheet(
      context: context,
      backgroundColor: const Color(0xFF111C2A),
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return SafeArea(
          child: Container(
            padding: const EdgeInsets.all(16),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      'Question History',
                      style: TextStyle(
                        color: Colors.white,
                        fontWeight: FontWeight.bold,
                        fontSize: 16,
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.close, color: Colors.white70, size: 20),
                      onPressed: () => Navigator.pop(context),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                if (_history.isEmpty)
                  const Padding(
                    padding: EdgeInsets.symmetric(vertical: 24),
                    child: Center(
                      child: Text(
                        'No previous questions yet.',
                        style: TextStyle(color: Color(0xFF64748B)),
                      ),
                    ),
                  )
                else
                  Flexible(
                    child: ListView.separated(
                      shrinkWrap: true,
                      itemCount: _history.length,
                      separatorBuilder: (context, _) => const Divider(color: Color(0xFF1E293B)),
                      itemBuilder: (context, index) {
                        final item = _history[index];
                        return ListTile(
                          contentPadding: EdgeInsets.zero,
                          title: Text(
                            item.question,
                            maxLines: 1,
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(
                              color: Color(0xFFF1F5F9),
                              fontSize: 14,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          subtitle: Text(
                            'Class ${item.grade} • ${item.subject}',
                            style: const TextStyle(
                              color: Color(0xFF64748B),
                              fontSize: 12,
                            ),
                          ),
                          trailing: const Icon(
                            Icons.arrow_forward_ios,
                            size: 14,
                            color: Color(0xFF64748B),
                          ),
                          onTap: () {
                            Navigator.pop(context);
                            _reopenHistoryItem(item);
                          },
                        );
                      },
                    ),
                  ),
              ],
            ),
          ),
        );
      },
    );
  }

  void _reopenHistoryItem(HistoryItem item) {
    setState(() {
      _selectedGrade = item.grade;
      _selectedSubject = item.subject;
      _messages.add(
        TutorMessage(
          id: 'msg_reopen_q_${DateTime.now().millisecondsSinceEpoch}',
          sender: MessageSender.student,
          content: item.question,
          timestamp: item.timestamp,
          grade: item.grade,
          subject: item.subject,
        ),
      );
      _messages.add(
        TutorMessage(
          id: 'msg_reopen_a_${DateTime.now().millisecondsSinceEpoch}',
          sender: MessageSender.tutor,
          content: item.answer,
          timestamp: item.timestamp,
          grade: item.grade,
          subject: item.subject,
          structuredResponse: ResponseParser.parse(item.answer),
        ),
      );
    });
    _scrollToBottom();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFF0F172A),
      appBar: PreferredSize(
        preferredSize: const Size.fromHeight(60),
        child: Container(
          decoration: const BoxDecoration(
            color: Color(0xFF0F172A),
            border: Border(
              bottom: BorderSide(
                color: Color(0xFF1E293B),
                width: 1,
              ),
            ),
          ),
          child: SafeArea(
            bottom: false,
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                children: [
                  // App Title
                  RichText(
                    text: const TextSpan(
                      children: [
                        TextSpan(
                          text: 'SHIK',
                          style: TextStyle(
                            color: Colors.white,
                            fontWeight: FontWeight.w800,
                            fontSize: 20,
                            letterSpacing: 1.2,
                          ),
                        ),
                        TextSpan(
                          text: 'SHA',
                          style: TextStyle(
                            color: Color(0xFF38BDF8),
                            fontWeight: FontWeight.w800,
                            fontSize: 20,
                            letterSpacing: 1.2,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const Spacer(),
                  // Grade selector chip
                  InkWell(
                    onTap: _showGradePicker,
                    borderRadius: BorderRadius.circular(20),
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                      decoration: BoxDecoration(
                        color: const Color(0xFF1E293B),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: const Color(0xFF334155)),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            'Class $_selectedGrade',
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 12.5,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          const SizedBox(width: 3),
                          const Icon(
                            Icons.keyboard_arrow_down,
                            color: Colors.white70,
                            size: 15,
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(width: 6),
                  // Subject selector chip
                  InkWell(
                    onTap: _showSubjectPicker,
                    borderRadius: BorderRadius.circular(20),
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 5),
                      decoration: BoxDecoration(
                        color: const Color(0xFF1E293B),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(color: const Color(0xFF334155)),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            _selectedSubject,
                            style: const TextStyle(
                              color: Colors.white,
                              fontSize: 12.5,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                          const SizedBox(width: 3),
                          const Icon(
                            Icons.keyboard_arrow_down,
                            color: Colors.white70,
                            size: 15,
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(width: 4),
                  // Compact actions menu
                  PopupMenuButton<String>(
                    icon: const Icon(Icons.more_vert, color: Colors.white70, size: 22),
                    color: const Color(0xFF1E293B),
                    onSelected: (val) {
                      if (val == 'history') {
                        _showHistoryModal();
                      } else if (val == 'new') {
                        _newConversation();
                      }
                    },
                    itemBuilder: (context) => [
                      const PopupMenuItem(
                        value: 'new',
                        child: Row(
                          children: [
                            Icon(Icons.refresh, color: Colors.white70, size: 18),
                            SizedBox(width: 10),
                            Text('New Conversation', style: TextStyle(color: Colors.white)),
                          ],
                        ),
                      ),
                      const PopupMenuItem(
                        value: 'history',
                        child: Row(
                          children: [
                            Icon(Icons.history, color: Colors.white70, size: 18),
                            SizedBox(width: 10),
                            Text('Question History', style: TextStyle(color: Colors.white)),
                          ],
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
      body: Column(
        children: [
          // Message feed
          Expanded(
            child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                if (message.sender == MessageSender.student) {
                  return _buildStudentBubble(message);
                } else {
                  return _buildTutorCard(message);
                }
              },
            ),
          ),
          // Input bar
          _buildInputBar(),
        ],
      ),
    );
  }

  Widget _buildStudentBubble(TutorMessage message) {
    return Align(
      alignment: Alignment.centerRight,
      child: Container(
        margin: const EdgeInsets.only(bottom: 8, left: 48),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        decoration: BoxDecoration(
          color: const Color(0xFF243447),
          borderRadius: BorderRadius.circular(16),
        ),
        child: Text(
          message.content,
          style: const TextStyle(
            color: Color(0xFFE2E8F0),
            fontSize: 14.5,
            height: 1.4,
          ),
        ),
      ),
    );
  }

  Widget _buildTutorCard(TutorMessage message) {
    // Check error
    if (message.error != null) {
      return Container(
        margin: const EdgeInsets.only(bottom: 16),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: const Color(0xFF2D1619),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: const Color(0xFF7F1D1D)),
        ),
        child: Row(
          children: [
            const Icon(Icons.error_outline, color: Color(0xFFF87171), size: 22),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                message.error!,
                style: const TextStyle(
                  color: Color(0xFFFCA5A5),
                  fontSize: 13.5,
                ),
              ),
            ),
          ],
        ),
      );
    }

    final structured = message.structuredResponse;
    final bool hasSections = structured != null && structured.hasStructuredSections;

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: const Color(0xFF111C2A),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: const Color(0xFF1E293B),
          width: 1.2,
        ),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (hasSections) ...[
            if (structured.definition != null && structured.definition!.isNotEmpty) ...[
              _buildSectionTitle('Definition:'),
              const SizedBox(height: 4),
              _buildSectionBody(structured.definition!),
              _buildSectionDivider(),
            ],
            if (structured.given != null && structured.given!.isNotEmpty) ...[
              _buildSectionTitle('Given:'),
              const SizedBox(height: 4),
              _buildSectionBody(structured.given!),
              _buildSectionDivider(),
            ],
            if (structured.formula != null && structured.formula!.isNotEmpty) ...[
              _buildSectionTitle('Formula: ${structured.formula!}'),
              _buildSectionDivider(),
            ],
            if (structured.steps.isNotEmpty) ...[
              _buildSectionTitle('Explanation:'),
              const SizedBox(height: 4),
              ...structured.steps.map((step) => Padding(
                    padding: const EdgeInsets.only(bottom: 4),
                    child: _buildSectionBody(step),
                  )),
              _buildSectionDivider(),
            ],
            if (structured.example != null && structured.example!.isNotEmpty) ...[
              _buildSectionTitle('Example:'),
              const SizedBox(height: 4),
              _buildSectionBody(structured.example!),
              _buildSectionDivider(),
            ],
            if (structured.summary != null && structured.summary!.isNotEmpty) ...[
              _buildSectionTitle('Summary:'),
              const SizedBox(height: 4),
              _buildSectionBody(structured.summary!),
            ],
            if (structured.finalAnswer != null && structured.finalAnswer!.isNotEmpty) ...[
              _buildSectionTitle('Final Answer:'),
              const SizedBox(height: 4),
              _buildSectionBody(structured.finalAnswer!),
            ],
          ] else ...[
            // Streaming or plain text fallback
            Text(
              message.content.trim().isEmpty && message.isGenerating
                  ? 'Analyzing question offline...'
                  : message.content.trim(),
              style: const TextStyle(
                color: Color(0xFFCBD5E1),
                fontSize: 14,
                height: 1.5,
              ),
            ),
          ],
          if (message.isGenerating) ...[
            const SizedBox(height: 12),
            Row(
              children: [
                const SizedBox(
                  width: 14,
                  height: 14,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    valueColor: AlwaysStoppedAnimation<Color>(Color(0xFF38BDF8)),
                  ),
                ),
                const SizedBox(width: 8),
                Text(
                  'Generating local response...',
                  style: TextStyle(
                    color: Colors.white.withValues(alpha: 0.5),
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ],
          if (!message.isGenerating && message.metrics != null) ...[
            const SizedBox(height: 12),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
              decoration: BoxDecoration(
                color: const Color(0xFF0F172A),
                borderRadius: BorderRadius.circular(6),
                border: Border.all(color: const Color(0xFF1E293B)),
              ),
              child: Text(
                '${message.metrics!.tokensPerSecond.toStringAsFixed(1)} tok/s • ${message.metrics!.completionTokens} tokens • 462 MB local GGUF',
                style: const TextStyle(
                  color: Color(0xFF64748B),
                  fontSize: 11,
                  fontFamily: 'monospace',
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildSectionTitle(String title) {
    return Text(
      title,
      style: const TextStyle(
        color: Color(0xFFF1F5F9),
        fontSize: 14,
        fontWeight: FontWeight.bold,
      ),
    );
  }

  Widget _buildSectionBody(String text) {
    return Text(
      text,
      style: const TextStyle(
        color: Color(0xFF94A3B8),
        fontSize: 13.5,
        height: 1.45,
      ),
    );
  }

  Widget _buildSectionDivider() {
    return const Padding(
      padding: EdgeInsets.symmetric(vertical: 8),
      child: Divider(
        color: Color(0xFF1E293B),
        thickness: 1,
        height: 1,
      ),
    );
  }

  Widget _buildInputBar() {
    return Container(
      padding: const EdgeInsets.fromLTRB(16, 8, 16, 16),
      decoration: const BoxDecoration(
        color: Color(0xFF0F172A),
        border: Border(
          top: BorderSide(
            color: Color(0xFF1E293B),
            width: 1,
          ),
        ),
      ),
      child: SafeArea(
        top: false,
        child: Row(
          children: [
            Expanded(
              child: Container(
                decoration: BoxDecoration(
                  color: const Color(0xFF131D2A),
                  borderRadius: BorderRadius.circular(24),
                  border: Border.all(color: const Color(0xFF243345)),
                ),
                padding: const EdgeInsets.symmetric(horizontal: 16),
                child: TextField(
                  controller: _inputController,
                  textInputAction: TextInputAction.send,
                  onSubmitted: (_) => _submitQuestion(),
                  style: const TextStyle(
                    color: Colors.white,
                    fontSize: 14,
                  ),
                  decoration: const InputDecoration(
                    hintText: 'Ask your question...',
                    hintStyle: TextStyle(
                      color: Color(0xFF64748B),
                      fontSize: 14,
                    ),
                    border: InputBorder.none,
                    isDense: true,
                    contentPadding: EdgeInsets.symmetric(vertical: 12),
                  ),
                ),
              ),
            ),
            const SizedBox(width: 8),
            InkWell(
              onTap: _isGenerating ? _stopGeneration : () => _submitQuestion(),
              borderRadius: BorderRadius.circular(12),
              child: Container(
                width: 44,
                height: 44,
                decoration: BoxDecoration(
                  color: _isGenerating ? const Color(0xFFEF4444) : const Color(0xFF38BDF8),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Icon(
                  _isGenerating ? Icons.stop_rounded : Icons.send_rounded,
                  color: Colors.white,
                  size: 20,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
