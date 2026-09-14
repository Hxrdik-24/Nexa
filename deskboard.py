from flask import Flask, render_template_string

app = Flask(__name__)


# Simple Dashboard HTML Structure (Tailwind included)
dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #050505; color: #00ff41; font-family: 'Courier New', monospace; }
        .card { background: #111; border: 1px solid #333; }
    </style>
</head>
<body class="p-8">
    <h1 class="text-3xl font-bold mb-6 text-center">NEXA V2 COMMAND CENTER</h1>
    
    <div class="grid grid-cols-2 gap-6">
        <!-- Logs Panel -->
        <div class="card p-4 h-96 overflow-y-auto">
            <h2 class="text-xl mb-2">System Logs</h2>
            <pre>{{ logs }}</pre>
        </div>
        
        <!-- Info Panel -->
        <div class="card p-4">
            <h2 class="text-xl mb-2">Current Status</h2>
            <p>Mode: <span class="text-blue-400">{{ mode }}</span></p>
            <p>Last Command: <span class="text-yellow-400">{{ last_cmd }}</span></p>
        </div>
    </div>
</body>
</html>
"""
from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def home():
    try:
        with open("brain/logs.txt", "r", encoding="utf-8") as f:
            data = f.read()
    except FileNotFoundError:
        data = "No logs found yet. [brain/logs.txt missing]"

    html_template = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NEXA V2 | Command Center</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            min-height: 100vh;
            margin: 0;
            overflow-x: hidden;
            font-family: "Courier New", monospace;
            color: #b8f6ff;
            background: radial-gradient(circle at 50% 50%, rgba(0, 110, 180, 0.12), transparent 40%), #020712;
        }
        body::before {
            content: "";
            position: fixed;
            inset: 0;
            background-image: linear-gradient(rgba(0, 180, 255, 0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 180, 255, 0.04) 1px, transparent 1px);
            background-size: 50px 50px;
            pointer-events: none;
            z-index: -1;
        }
        .card {
            position: relative;
            background: rgba(5, 15, 30, 0.75);
            border: 1px solid rgba(0, 200, 255, 0.25);
            border-radius: 16px;
            backdrop-filter: blur(15px);
            box-shadow: 0 0 20px rgba(0, 170, 255, 0.08), inset 0 0 20px rgba(0, 100, 200, 0.03);
            overflow: hidden;
        }
        .card::before {
            content: "";
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 1px;
            background: linear-gradient(90deg, transparent, #00d9ff, transparent);
        }
        .nexa-container {
            position: relative;
            width: 420px;
            height: 420px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .mist {
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 50%;
            filter: blur(25px);
            background: radial-gradient(circle at 20% 50%, rgba(0, 180, 255, 0.45), transparent 25%), radial-gradient(circle at 80% 30%, rgba(0, 100, 255, 0.4), transparent 30%), radial-gradient(circle at 60% 90%, rgba(0, 220, 255, 0.3), transparent 25%);
            animation: mistMove 7s ease-in-out infinite alternate;
        }
        .outer-ring {
            position: absolute;
            width: 370px;
            height: 370px;
            border-radius: 50%;
            border: 2px solid rgba(0, 210, 255, 0.65);
            box-shadow: 0 0 15px #00c8ff, 0 0 50px rgba(0, 100, 255, 0.5);
            animation: rotate 8s linear infinite;
        }
        .outer-ring::after {
            content: "";
            position: absolute;
            width: 80px;
            height: 80px;
            top: -5px;
            left: 50%;
            transform: translateX(-50%);
            border-top: 4px solid #ffffff;
            border-radius: 50%;
            filter: drop-shadow(0 0 10px #00d9ff);
        }
        .middle-ring {
            position: absolute;
            width: 305px;
            height: 305px;
            border-radius: 50%;
            border: 2px dashed rgba(0, 220, 255, 0.8);
            animation: rotateReverse 12s linear infinite;
        }
        .inner-ring {
            position: absolute;
            width: 240px;
            height: 240px;
            border-radius: 50%;
            border: 2px solid #00d9ff;
            background: radial-gradient(circle, rgba(0, 130, 255, 0.18), transparent 70%);
            box-shadow: 0 0 25px #00d9ff, inset 0 0 35px rgba(0, 180, 255, 0.3);
            animation: pulse 2.5s ease-in-out infinite;
        }
        .nexa-text {
            position: relative;
            z-index: 10;
            text-align: center;
            color: #00d9ff;
            text-shadow: 0 0 10px #00d9ff, 0 0 30px #0077ff;
        }
        .nexa-text h1 {
            margin: 0;
            font-size: 64px;
            letter-spacing: 12px;
            font-weight: bold;
        }
        .nexa-text p {
            margin-top: 12px;
            font-size: 11px;
            letter-spacing: 6px;
            color: #a9efff;
        }
        .status-online {
            margin-top: 20px;
            color: #00ff9d;
            font-size: 11px;
            letter-spacing: 3px;
            animation: blink 1.5s infinite;
        }
        .particle {
            position: absolute;
            width: 4px;
            height: 4px;
            background: #00d9ff;
            border-radius: 50%;
            box-shadow: 0 0 12px #00d9ff;
            animation: float 4s infinite ease-in-out;
        }
        .terminal {
            background: #01050c;
            border: 1px solid rgba(0, 200, 255, 0.2);
            border-radius: 10px;
            padding: 15px;
            color: #8cecff;
        }
        .command-input {
            width: 100%;
            padding: 14px;
            background: #020914;
            border: 1px solid rgba(0, 217, 255, 0.4);
            border-radius: 8px;
            outline: none;
            color: #00eaff;
            font-family: inherit;
            transition: 0.3s;
        }
        .command-input:focus {
            border-color: #00d9ff;
            box-shadow: 0 0 20px rgba(0, 217, 255, 0.2);
        }
        .command-btn {
            padding: 14px 25px;
            border: 1px solid #00d9ff;
            border-radius: 8px;
            background: rgba(0, 217, 255, 0.08);
            color: #00d9ff;
            font-family: inherit;
            cursor: pointer;
            transition: 0.3s;
        }
        .command-btn:hover {
            background: #00d9ff;
            color: #020712;
            box-shadow: 0 0 25px #00d9ff;
        }
        @keyframes rotate { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes rotateReverse { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
        @keyframes pulse { 0%, 100% { transform: scale(1); box-shadow: 0 0 20px #00d9ff, inset 0 0 30px rgba(0, 200, 255, 0.2); } 50% { transform: scale(1.06); box-shadow: 0 0 50px #00d9ff, 0 0 100px rgba(0, 100, 255, 0.6), inset 0 0 50px rgba(0, 200, 255, 0.4); } }
        @keyframes mistMove { 0% { transform: rotate(0deg) scale(1); opacity: 0.45; } 100% { transform: rotate(180deg) scale(1.2); opacity: 0.9; } }
        @keyframes float { 0%, 100% { transform: translateY(0); opacity: 0.3; } 50% { transform: translateY(-35px); opacity: 1; } }
        @keyframes blink { 50% { opacity: 0.35; } }
        @media (max-width: 768px) {
            .nexa-container { transform: scale(0.75); margin: -40px auto; }
        }
    </style>
</head>
<body class="p-4 md:p-8">
    <header class="mb-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <div>
            <h1 class="text-3xl font-bold tracking-widest text-cyan-300">NEXA V2</h1>
            <p class="text-xs tracking-[0.3em] text-cyan-700 mt-2">AI COMMAND CENTER</p>
        </div>
        <div class="flex items-center gap-3 text-xs">
            <span class="w-3 h-3 rounded-full bg-green-400 animate-pulse"></span>
            <span class="text-green-400">SYSTEM ONLINE</span>
        </div>
    </header>

    <main class="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <section class="card min-h-[600px] flex flex-col items-center justify-center p-6">
            <div class="absolute top-6 left-6 text-xs text-cyan-700">CORE MODULE</div>
            <div class="absolute top-6 right-6 text-xs text-green-400">● ACTIVE</div>
            
            <div class="nexa-container">
                <div class="mist"></div>
                <div class="outer-ring"></div>
                <div class="middle-ring"></div>
                <div class="inner-ring"></div>
                <div class="nexa-text">
                    <h1>NEXA</h1>
                    <p>AI ASSISTANT</p>
                    <div class="status-online">● LISTENING</div>
                </div>
                <div class="particle" style="top:15%; left:10%;"></div>
                <div class="particle" style="top:75%; left:15%; animation-delay:1s;"></div>
                <div class="particle" style="top:12%; right:12%; animation-delay:2s;"></div>
                <div class="particle" style="bottom:18%; right:12%; animation-delay:0.5s;"></div>
            </div>

            <div class="grid grid-cols-3 gap-4 w-full max-w-md mt-6 text-center">
                <div class="terminal">
                    <div class="text-xs text-cyan-700">MODE</div>
                    <div class="mt-2 text-cyan-300">{{ mode }}</div>
                </div>
                <div class="terminal">
                    <div class="text-xs text-cyan-700">STATUS</div>
                    <div class="mt-2 text-green-400">ONLINE</div>
                </div>
                <div class="terminal">
                    <div class="text-xs text-cyan-700">VERSION</div>
                    <div class="mt-2 text-cyan-300">V2.0</div>
                </div>
            </div>
        </section>

        <section class="flex flex-col gap-6">
            <div class="card p-6">
                <h2 class="text-xl text-cyan-300 mb-6">CURRENT STATUS</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div class="terminal">
                        <div class="text-xs text-cyan-700">CURRENT MODE</div>
                        <div class="text-lg text-cyan-300 mt-2">{{ mode }}</div>
                    </div>
                    <div class="terminal">
                        <div class="text-xs text-cyan-700">LAST COMMAND</div>
                        <div class="text-sm text-yellow-300 mt-2 break-all">{{ last_cmd }}</div>
                    </div>
                </div>
            </div>

            <!-- System Logs -->
            <div class="card p-6 flex-1">
                <div class="flex justify-between items-center mb-5">
                    <h2 class="text-xl text-cyan-300">SYSTEM LOGS</h2>
                    <span class="text-xs text-green-400">● LIVE</span>
                </div>
                <div class="terminal h-72 overflow-y-auto text-sm">
                    <pre class="whitespace-pre-wrap font-mono">{{ logs }}</pre>
                </div>
            </div>

            <div class="card p-6">
                <h2 class="text-xl text-cyan-300 mb-5">COMMAND TERMINAL</h2>
                <div class="flex flex-col md:flex-row gap-3">
                    <input type="text" id="commandInput" class="command-input" placeholder="Enter command for Nexa...">
                    <button id="sendCommand" class="command-btn">EXECUTE</button>
                </div>
            </div>
        </section>
    </main>

    <footer class="text-center text-xs text-cyan-900 tracking-widest mt-8">
        NEXA AI SYSTEM • COMMAND CENTER • SECURE CONNECTION
    </footer>

    <script>
        const commandInput = document.getElementById("commandInput");
        const sendButton = document.getElementById("sendCommand");

        function sendCommand() {
            const command = commandInput.value.trim();
            if (!command) return;
            console.log("Command sent to Nexa:", command);
            commandInput.value = "";
        }

        sendButton.addEventListener("click", sendCommand);
        commandInput.addEventListener("keypress", function(event) {
            if (event.key === "Enter") {
                sendCommand();
            }
        });
    </script>
</body>
</html>
    """
    return render_template_string(html_template, logs=data, mode='normal', last_cmd="Hello NEXA")

if __name__ == "__main__":
    app.run(debug=True)

@app.route('/desk')
def desk():
  return render_template_string(dashboard_html,mode='normal',last_cmd="Hello NEXA")
if __name__ == "__main__":
  app.run(debug=True, port=2424, host="0.0.0.0")