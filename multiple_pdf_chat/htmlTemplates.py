css = """
<style>
.chat-message {
    padding: 10px;
    margin-bottom: 10px;
    max-width: 100%;
}

.chat-message.user {
    border-radius: 10px;
    background-color: #f2f2f2;
    display: flex;
    align-items: center;
}

.chat-message.bot {
    border-radius: 10px;
    background-color: #e0f2ff;
    display: flex;
    align-items: center;
}

.chat-message img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 10px;
    object-fit: cover;
}

.chat-message .message-text {
    color: #333333;
}

.chat-message.user .message-time {
    font-size: 0.8em;
    color: #999999;
    margin-left: auto;
}

.chat-message.bot .message-time {
    font-size: 0.8em;
    color: #999999;
    margin-right: auto;
}
"""

bot_template = """
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://images.unsplash.com/photo-1586512361825-08f9d0f7102b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1335&q=80">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
    <div class="avatar">
        <img src="https://images.unsplash.com/photo-1572114760509-91d07e2941e3?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=927&q=80">
    </div>
    <div class="message">{{MSG}}</div>
</div>
"""
