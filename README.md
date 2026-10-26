# Paket Ruang Pikir

Semua aset brand Ruang Pikir dalam satu folder. Kirim folder ini (atau zip-nya) ke Claude Code, lalu mulai dengan:

> "Baca CLAUDE.md. Website sudah live di ruangpikir.id (VPS); update dengan `ruangpikir-deploy`."

Untuk episode baru:

> "Baca CLAUDE.md lalu pakai video-engine/PROMPT_VIDEO_BARU.md. Topik: ..."

| Folder | Untuk apa |
|---|---|
| `CLAUDE.md` | Instruksi utama untuk Claude Code |
| `website/` | Website (beranda, halaman episode, data `episodes.json`) + cara deploy |
| `tools/` | `build_site.py` untuk membangun halaman episode & gambar preview |
| `deploy/` | Skrip pemasangan & update di VPS (`ruangpikir-deploy`), statistik |
| `brand/` | Logo + panduan brand |
| `content/` | Profil IG, caption EP01 & EP02, bank ide |
| `videos/` | EP01 & EP02 siap upload |
| `video-engine/` | Mesin pembuat video + prompt episode baru |

API key **tidak** disertakan. Saat dibutuhkan: `export GEMINI_API_KEY=...`
