# Advanced AI Architecture Roadmap

To push the backend from a "great prototype" to an **Elite Enterprise AI Engine**, we must evolve the core AI architecture. Currently, our system uses a linear pipeline (`Scraper` ➔ `Analyzer` ➔ `Recommender`). Here is how we can supercharge the AI logic:

## 1. RAG-Powered Memory (Retrieval-Augmented Generation)
**Kelemahan Saat Ini:** AI kita (Recommender) hanya melihat data saat ini (*snapshot* tunggal) untuk membuat keputusan. Ia tidak memiliki "ingatan" tentang masa lalu.
**Peningkatan AI:** 
Sebelum memberikan rekomendasi, *Agent* akan melakukan pencarian (*Query*) ke **Pinecone** untuk membaca sejarah harga kompetitor atau membaca rekomendasi sebelumnya.
*Contoh Prompt AI: "Dua minggu lalu harga kompetitor adalah Rp 150.000, sekarang Rp 120.000. Mereka sedang perang harga. Rekomendasi: Jangan ikut banting harga, fokus ke kualitas."*

## 2. Self-Reflection & Critique Loop (LangGraph Advanced)
**Kelemahan Saat Ini:** Apapun keputusan yang dibuat oleh *Recommender*, langsung diterima oleh sistem. Bagaimana jika keputusannya merugikan margin perusahaan?
**Peningkatan AI:** 
Menambahkan **Critique Node**. Setelah *Recommender* membuat keputusan (misal: "Turunkan harga jadi Rp 10.000"), *Critique Agent* akan mengevaluasinya berdasarkan aturan bisnis (misal: "Batas margin adalah Rp 15.000. Keputusan ini ditolak"). LangGraph akan memutar kembali arah (*loop*) ke *Recommender* untuk merevisi strateginya sampai lolos evaluasi.

## 3. Parallel Multi-Agent Swarm
**Kelemahan Saat Ini:** Kita hanya mengandalkan satu jalur *scraping* (halaman e-commerce).
**Peningkatan AI:** 
Menggunakan kapabilitas *Parallel Branching* di LangGraph.
- **Agent A (Pricing Scout)**: Mengekstrak harga dari e-commerce (Tokopedia/Amazon).
- **Agent B (Brand Sentinel)**: Menggunakan Bright Data SERP API untuk mencari berita/artikel terbaru atau keluhan di forum (Reddit/X) tentang kompetitor tersebut.
- **Synthesizer Node**: Menggabungkan hasil Agent A dan Agent B menjadi satu *super-report*.

## 4. Native Structured Outputs (Pydantic)
**Kelemahan Saat Ini:** Kita menggunakan *Regular Expression* (Regex) untuk mengekstrak JSON dari balasan AI. Ini bisa rapuh jika LLM berhalusinasi.
**Peningkatan AI:** 
Mengintegrasikan kapabilitas **LLM Native Tool Calling (Structured Output)** menggunakan Pydantic. AI dipaksa secara arsitektur oleh OpenAI API untuk selalu merespons dengan JSON yang formatnya 100% valid dan presisi tanpa perlu *Regex*.
