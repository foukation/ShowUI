import threading
from app import build_demo
from ShowUI_api import app


def run_flask():
    try:
        # 使用 threaded=True 支持并发请求处理
        app.run(host='0.0.0.0', port=11503, debug=False, threaded=True)
    except Exception as e:
        print(f"Flask server error: {e}")


if __name__ == "__main__":
    # 创建 Flask 子线程
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

    # 给 Flask 一些启动时间
    import time

    time.sleep(2)

    # 在主线程中运行 Gradio
    demo = build_demo(embed_mode=False)
    demo.queue(api_open=False).launch(
        server_name="0.0.0.0",
        server_port=11502,
        ssr_mode=True,
        debug=True,
        share=True,
        show_error=True,
        show_api=False,
    )