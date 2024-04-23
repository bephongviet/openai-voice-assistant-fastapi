# openai-voice-assistant-fastapi
Sử dụng open ai và google text to speech để làm voice assistant. Đây là fastapi backend với python3

Ví dụ cách gọi qua curl:

```
curl --location 'http://127.0.0.1:8000/assist/' \
--form 'voice=@"/../path/to.../uservoice.m4a"'
```

Developed together with LinxHQ https://linxhq.com
