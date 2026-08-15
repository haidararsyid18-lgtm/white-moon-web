    from flask import Flask, render_template, request, jsonify
    import re, json, os, datetime, random
    app = Flask(__name__)

    class WhiteMoon:
        def __init__(self):
            self.nama_ai = "WHITE_MOON"
            self.daftar_ai = ["DOLA AI", "META AI", "NOVA AI", "SIGMA AI", "OMEGA AI"]
            self.bobot_ai = {"DOLA AI":1.0, "META AI":1.0, "NOVA AI":1.0, "SIGMA AI":1.2, "OMEGA AI":1.3}
            self.memori_jangka_panjang = {}
            self.file_memori = "memori_whitemoon.json"
            self.kode_aktif = "# Versi 1.0: Kerangka dasar WHITE_MOON\n"
            self.versi = 4.0
            self.developer = {"tingkat_kepintaran": 80, "auto_learning": True}
            self.muat_memori()

        def muat_memori(self):
            if os.path.exists(self.file_memori):
                with open(self.file_memori, "r", encoding="utf-8") as f:
                    self.memori_jangka_panjang = json.load(f)

        def simpan_memori(self):
            with open(self.file_memori, "w", encoding="utf-8") as f:
                json.dump(self.memori_jangka_panjang, f, indent=4, ensure_ascii=False)

        def debat_api(self, topik):
            if len(topik) < 5: return {"error": "Topik terlalu singkat"}
            if self.developer["auto_learning"] and topik in self.memori_jangka_panjang:
                data = self.memori_jangka_panjang[topik]
                return {"from_memory": True, "disetujui": data["disetujui"], "jumlah_setuju": data["jumlah_setuju"]}
            hasil_vote = {}
            for ai in self.daftar_ai:
                peluang = self.bobot_ai[ai] * self.developer["tingkat_kepintaran"] / 100
                hasil_vote[ai] = random.random() < peluang
            jumlah_setuju = sum(1 for v in hasil_vote.values() if v)
            lolos = jumlah_setuju >= 3
            self.memori_jangka_panjang[topik] = {"jumlah_setuju": jumlah_setuju, "disetujui": lolos, "waktu": datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}
            self.simpan_memori()
            return {"from_memory": False, "disetujui": lolos, "jumlah_setuju": jumlah_setuju, "vote": hasil_vote}

        def analisis_api(self):
            total_fungsi = len(re.findall(r'def\s+\w+', self.kode_aktif))
            total_baris = len(self.kode_aktif.split('\n'))
            skor = max(0, 100 - total_baris // 10)
            return {"skor_kualitas": skor, "total_fungsi": total_fungsi, "total_baris": total_baris}

    tim = WhiteMoon()

    @app.route("/")
    def index():
        return render_template("index.html", versi=tim.versi)

    @app.route("/api/debat", methods=["POST"])
    def api_debat():
        topik = request.json.get("topik", "")
        return jsonify(tim.debat_api(topik))

    @app.route("/api/analisis", methods=["GET"])
    def api_analisis():
        return jsonify(tim.analisis_api())

    @app.route("/api/ingat", methods=["GET"])
    def api_ingat():
        return jsonify(tim.memori_jangka_panjang)

    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
