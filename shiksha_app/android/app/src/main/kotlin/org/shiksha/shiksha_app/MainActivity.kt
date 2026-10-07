package org.shiksha.shiksha_app

import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import org.shiksha.tutor.ShikshaPlatformChannel

class MainActivity : FlutterActivity() {
    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)
        ShikshaPlatformChannel(flutterEngine.dartExecutor.binaryMessenger, applicationContext)
    }
}
