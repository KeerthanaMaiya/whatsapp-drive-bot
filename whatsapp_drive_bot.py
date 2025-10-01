from flask import Flask, jsonify 
from flask_cors import CORS 
from datetime import datetime 
 
app = Flask(__name__) 
CORS(app) 
 
class BotState: 
    def __init__(self): 
        self.is_running = False 
        self.is_connected = False 
        self.qr_code = None 
 
bot_state = BotState() 
 
@app.route('/') 
def home(): 
    return ''' 
    <!DOCTYPE html> 
    <html> 
    <head> 
        <title>WhatsApp Drive Bot</title> 
        <style> 
            body { font-family: Arial, sans-serif; padding: 20px; } 
            .container { max-width: 800px; margin: 0 auto; } 
            .header { background: #25D366; color: white; padding: 20px; border-radius: 10px; text-align: center; } 
            .btn { padding: 10px 20px; margin: 5px; border: none; border-radius: 5px; cursor: pointer; } 
            .btn-start { background: #28a745; color: white; } 
            .btn-stop { background: #dc3545; color: white; } 
            .btn-qr { background: #007bff; color: white; } 
            .status { background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 10px 0; } 
        </style> 
    </head> 
    <body> 
        <div class="container"> 
            <div class="header"> 
                <h1>WhatsApp Drive Bot</h1> 
                <p>Automatically save WhatsApp files to Google Drive</p> 
            </div> 
            <div class="status"> 
                <h3>Bot Status</h3> 
                <p>Bot Status: <span id="botStatus">Stopped</span></p> 
                <p>WhatsApp: <span id="whatsappStatus">Disconnected</span></p> 
                <p>Last Update: <span id="lastUpdate">-</span></p> 
            </div> 
            <div> 
                <button class="btn btn-start" onclick="startBot()">Start Bot</button> 
                <button class="btn btn-stop" onclick="stopBot()">Stop Bot</button> 
                <button class="btn btn-qr" onclick="getQRCode()">Get QR Code</button> 
                <button class="btn" onclick="refreshStatus()">Refresh Status</button> 
            </div> 
            <div id="qrSection" style="display:none; margin-top:20px; padding:20px; background:#f8f9fa; border-radius:5px;"> 
                <h3>QR Code</h3> 
                <div id="qrCode"></div> 
            </div> 
        </div> 
        <script> 
            async function refreshStatus() { 
                const response = await fetch('/status'); 
                const status = await response.json(); 
                document.getElementById('botStatus').textContent = status.is_running ? 'Running' : 'Stopped'; 
                document.getElementById('whatsappStatus').textContent = status.whatsapp_status; 
                document.getElementById('lastUpdate').textContent = status.timestamp; 
            } 
 
            async function startBot() { 
                const response = await fetch('/start', { method: 'POST' }); 
                const result = await response.json(); 
                alert(result.message); 
                refreshStatus(); 
            } 
 
            async function stopBot() { 
                const response = await fetch('/stop', { method: 'POST' }); 
                const result = await response.json(); 
                alert(result.message); 
                refreshStatus(); 
            } 
 
            async function getQRCode() { 
                const response = await fetch('/qr'); 
                const result = await response.json(); 
                if (result.status === 'success') { 
                    document.getElementById('qrSection').style.display = 'block'; 
                    document.getElementById('qrCode').innerHTML = 'QR Code: ' + result.qr_data; 
                } else { 
                    alert(result.message); 
                } 
            } 
 
            // Refresh status every 3 seconds 
            setInterval(refreshStatus, 3000); 
            refreshStatus(); 
        </script> 
    </body> 
    </html> 
    ''' 
 
@app.route('/status') 
def status(): 
    return jsonify({ 
        'is_running': bot_state.is_running, 
        'is_connected': bot_state.is_connected, 
        'whatsapp_status': 'connected' if bot_state.is_connected else 'disconnected', 
        'timestamp': datetime.now().isoformat() 
    }) 
 
@app.route('/start', methods=['POST']) 
def start_bot(): 
    bot_state.is_running = True 
    bot_state.qr_code = f'QR_CODE_{datetime.now().strftime("%Y%m%d%H%M%S")}' 
    return jsonify({'status': 'success', 'message': 'Bot started successfully!'}) 
 
@app.route('/stop', methods=['POST']) 
def stop_bot(): 
    bot_state.is_running = False 
    bot_state.is_connected = False 
    bot_state.qr_code = None 
    return jsonify({'status': 'success', 'message': 'Bot stopped successfully!'}) 
 
@app.route('/qr') 
def get_qr(): 
    if bot_state.qr_code: 
        return jsonify({'status': 'success', 'qr_data': bot_state.qr_code}) 
    else: 
        return jsonify({'status': 'error', 'message': 'Start the bot first to get QR code'}) 
 
if __name__ == '__main__': 
    app.run(host='0.0.0.0', port=5000, debug=True) 
