import os
from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, request, render_template, flash, session, redirect, url_for
from openai import OpenAI, OpenAIError
# For PDF generation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import simpleSplit
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# PDF font settings
# Register a modern TrueType font (place the .ttf file in a 'fonts' folder)
FONT_PATH = os.path.join(os.path.dirname(__file__), 'fonts', 'Roboto-Regular.ttf')
try:
    pdfmetrics.registerFont(TTFont('Roboto', FONT_PATH))
    FONT_NAME = 'Roboto'
except Exception as e:
    # Fallback to Helvetica if custom font fails
    print(f"Warning: could not register Roboto font ({e}), falling back to Helvetica.")
    FONT_NAME = 'Helvetica'

FONT_SIZE = 9  # smaller font size for better fit
LINE_HEIGHT = FONT_SIZE + 4  # increased line spacing
MARGIN_X = 50  # horizontal margin
MARGIN_Y = 50  # vertical margin


def create_app():
    # Load environment variables
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not set in environment variables!")

    client = OpenAI(api_key=api_key)
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", "devkey")

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    @app.route("/", methods=["GET", "POST"])
    def index():
        result = None
        system_prompt = ""
        user_prompt = ""

        if "messages" not in session:
            session["messages"] = []
            session["system_set"] = False

        if request.method == "POST":
            if request.form.get("reset_conversation"):
                session.pop("messages", None)
                session.pop("system_set", None)
                flash("Conversation reset.", "success")
                return redirect(url_for("index"))

            if request.form.get("save_conversation"):
                messages = session.get("messages", [])
                if not messages:
                    flash("No conversation to save.", "warning")
                else:
                    save_type = request.form.get("save_type", "full")
                    save_format = request.form.get("save_format", "txt")
                    custom_name = request.form.get("save_filename", "").strip()
                    base = custom_name or datetime.now().strftime("conversation_%Y%m%d_%H%M%S")
                    ext = ".pdf" if save_format == "pdf" else ".txt"
                    filename = base if base.lower().endswith(ext) else base + ext

                    if save_type == "assistant":
                        lines = [m['content'] for m in messages if m['role'] == 'assistant']
                        if not lines:
                            flash("No assistant messages to save.", "warning")
                            return render_template("index.html", history=messages,
                                                   system_prompt=system_prompt, user_prompt=user_prompt)
                        labeled = [f"AI: {l}" for l in lines]
                    else:
                        labeled = [f"{m['role'].upper()}: {m['content']}" for m in messages]

                    save_dir = "saved_responses"
                    os.makedirs(save_dir, exist_ok=True)
                    path = os.path.join(save_dir, filename)

                    if save_format == "pdf":
                        try:
                            # Generate PDF with wrapped text and improved layout
                            c = Canvas(path, pagesize=letter)
                            width, height = letter
                            max_width = width - 2 * MARGIN_X

                            # Begin text
                            text_obj = c.beginText(MARGIN_X, height - MARGIN_Y)
                            text_obj.setFont(FONT_NAME, FONT_SIZE)
                            text_obj.setLeading(LINE_HEIGHT)

                            for line in labeled:
                                wrapped = simpleSplit(line, FONT_NAME, FONT_SIZE, max_width)
                                for segment in wrapped:
                                    if text_obj.getY() < MARGIN_Y:
                                        c.drawText(text_obj)
                                        c.showPage()
                                        text_obj = c.beginText(MARGIN_X, height - MARGIN_Y)
                                        text_obj.setFont(FONT_NAME, FONT_SIZE)
                                        text_obj.setLeading(LINE_HEIGHT)
                                    text_obj.textLine(segment)
                                # add blank line between messages
                                text_obj.textLine("")

                            c.drawText(text_obj)
                            c.save()
                        except Exception as pdf_err:
                            flash(f"PDF generation failed: {pdf_err}", "danger")
                    else:
                        # Save as TXT
                        try:
                            with open(path, "w", encoding="utf-8") as f:
                                f.write("".join(labeled))
                        except Exception as txt_err:
                            flash(f"Text save failed: {txt_err}", "danger")

                    flash(f"Conversation saved as {filename}", "success")
                    return redirect(url_for("index"))
            else:
                # Chat flow
                system_prompt = request.form.get("system_prompt", "").strip()
                user_prompt = request.form.get("user_prompt", "").strip()
                if not user_prompt:
                    flash("Please enter a user prompt!", "warning")
                else:
                    try:
                        msgs = session.get("messages")
                        if system_prompt and not session.get("system_set"):
                            msgs.insert(0, {"role": "system", "content": system_prompt})
                            session["system_set"] = True
                        msgs.append({"role": "user", "content": user_prompt})
                        resp = client.chat.completions.create(
                            model="gpt-4.1-nano", messages=msgs,
                            max_tokens=3000, temperature=0.7
                        )
                        assistant_msg = resp.choices[0].message.content.strip()
                        msgs.append({"role": "assistant", "content": assistant_msg})
                        session["messages"] = msgs
                        result = assistant_msg
                    except OpenAIError as e:
                        flash(f"API error: {e}", "danger")

        history = session.get("messages", [])
        return render_template(
            "index.html", result=result, history=history,
            system_prompt=system_prompt, user_prompt=user_prompt
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)
