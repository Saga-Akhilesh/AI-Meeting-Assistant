from hume_voice import speak_hume
from gemini_llm import answer_doubt

def run_qa_voice(slides, hume_key: str):
    from stt_vosk import record_and_transcribe

    all_context = "\n\n".join([s["context"] for s in slides])

    speak_hume(hume_key, "Thank you everyone. Now we will move to the Q and A session.")
    speak_hume(hume_key, "Press Enter to ask a question.")

    while True:
        cmd = input("\nPress ENTER to record question (or type 'exit' to stop): ").strip().lower()
        if cmd in ["exit", "stop", "end", "quit"]:
            speak_hume(hume_key, "Thank you everyone. I am ending the session now.")
            break

        question = record_and_transcribe(seconds=8)
        print("🧠 RAW TRANSCRIPTION:", repr(question))

        if not question or len(question) < 3:
         speak_hume(hume_key, "I could not hear the question clearly. Please try again.")
         continue


        ans = answer_doubt(all_context, question)
        speak_hume(hume_key, ans)
