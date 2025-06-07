from openai import OpenAI
from config import OPENROUTER_API_KEY, OPENROUTER_API_URL
from models import get_all_films  # Jika perlu akses DB

client = OpenAI(
    base_url=OPENROUTER_API_URL,
    api_key=OPENROUTER_API_KEY
)

def query_deepseek(prompt):
    try:
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528-qwen3-8b:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Maaf, AI error: {e}"

def query_deepseek(prompt):
    try:
        films = get_all_films()
        # Limit supaya prompt tidak terlalu panjang (misal 10 film saja)
        film_list_str = "\n".join(f"- {f['title']} (genre: {f['genre']})" for f in films)
        system_content = (
            "Kamu adalah Festy AI, asisten FestFlix. "
            "Jawab hanya seputar penggunaan FestFlix (fitur, langganan, review, rekomendasi film) atau bahas film-film dunia. "
            "Jika pertanyaan tidak berhubungan, jawab: 'Maaf, saya hanya menjawab pertanyaan tentang FestFlix atau film.' "
            "FestFlix adalah platform streaming film festival karya mahasiswa. "
            "Fitur: subscription murah, 2 tontonan gratis/hari, AI chat rekomendasi, dll. "
            "Saya ahli dalam memberikan rekomendasi film, menjelaskan fitur FestFlix, dan membantu pengguna memahami cara menggunakan platform ini. "
            "Saya bisa menjawab seluruh pertanyaan yang berhubungan dengan dunia film, termasuk rekomendasi, genre, dan informasi umum tentang film di dunia bahkan diluar konteks festflix.\n"
            f"Berikut 5 film terbaru FestFlix:\n{film_list_str}\n"
            "Jika ada pertanyaan tentang rekomendasi, berikan jawaban berdasarkan daftar film di atas dulu."
            "gaya bahasa santai dan selalu merapikan format penulisan. Gunakan kalimat paduh dan jelas, hindari singkatan yang tidak umum. "
        )
        completion = client.chat.completions.create(
            model="deepseek/deepseek-r1-0528-qwen3-8b:free",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Maaf, AI error: {e}"

def rule_based_reply(msg):
    msg = msg.lower()
    if "rekomendasi" in msg:
        return "Coba tonton: Drama Festival, Aksi Hebat, atau Komedi Segar!"
    elif "genre" in msg:
        parts = msg.split()
        if len(parts) >= 2:
            genre = parts[-1].capitalize()
            matched = [f['title'] for f in get_all_films() if f['genre'] == genre]
            if matched:
                return f"Film genre {genre}: " + ", ".join(matched)
            else:
                return f"Tidak ada film dengan genre {genre}."
        else:
            return "Ketik 'genre <nama genre>' untuk cari film."
    return "Maaf, Festy AI sedang sibuk. Coba lagi nanti atau ketik 'rekomendasi'."
