import os, json, random, asyncio, logging, urllib.request
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv

load_dotenv(os.path.expanduser("~/.env"))

TOKEN   = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
HOUR    = int(os.getenv("SEND_HOUR", "6"))
MINUTE  = int(os.getenv("SEND_MINUTE", "0"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

KANJI = [
    ("日","にち/ひ","hari/matahari","今日はいい日です。","Kyou wa ii hi desu.","Hari ini hari yang baik."),
    ("月","つき/げつ","bulan","月がきれいです。","Tsuki ga kirei desu.","Bulannya indah."),
    ("火","ひ/か","api","火は熱い。","Hi wa atsui.","Api itu panas."),
    ("水","みず/すい","air","水を飲みます。","Mizu o nomimasu.","Saya minum air."),
    ("木","き/もく","pohon","木が大きい。","Ki ga ookii.","Pohonnya besar."),
    ("金","かね/きん","emas/uang","お金がない。","Okane ga nai.","Tidak punya uang."),
    ("土","つち/ど","tanah","土をさわります。","Tsuchi o sawarimasu.","Menyentuh tanah."),
    ("山","やま/さん","gunung","山に登ります。","Yama ni noborimasu.","Mendaki gunung."),
    ("川","かわ/せん","sungai","川で泳ぎます。","Kawa de oyogimasu.","Berenang di sungai."),
    ("人","ひと/じん","orang","あの人は誰ですか。","Ano hito wa dare desuka.","Orang itu siapa?"),
    ("口","くち/こう","mulut","口を開けてください。","Kuchi o akete kudasai.","Tolong buka mulut."),
    ("手","て/しゅ","tangan","手を洗います。","Te o araimasu.","Mencuci tangan."),
    ("目","め/もく","mata","目が痛い。","Me ga itai.","Mata sakit."),
    ("耳","みみ/じ","telinga","耳で聞きます。","Mimi de kikimasu.","Mendengar dengan telinga."),
    ("足","あし/そく","kaki","足が速い。","Ashi ga hayai.","Kakinya cepat."),
    ("子","こ/し","anak","子どもが遊んでいます。","Kodomo ga asonde imasu.","Anak-anak sedang bermain."),
    ("女","おんな/じょ","wanita","女の人です。","Onna no hito desu.","Itu wanita."),
    ("男","おとこ/だん","laki-laki","男の子です。","Otoko no ko desu.","Itu anak laki-laki."),
    ("父","ちち/ふ","ayah","父は会社員です。","Chichi wa kaishain desu.","Ayah saya karyawan."),
    ("母","はは/ぼ","ibu","母は料理が上手です。","Haha wa ryouri ga jouzu desu.","Ibu pandai memasak."),
    ("大","おお/だい","besar","大きい犬です。","Ookii inu desu.","Anjing yang besar."),
    ("小","ちい/しょう","kecil","小さい猫です。","Chiisai neko desu.","Kucing yang kecil."),
    ("中","なか/ちゅう","tengah/dalam","箱の中にあります。","Hako no naka ni arimasu.","Ada di dalam kotak."),
    ("上","うえ/じょう","atas","机の上に本がある。","Tsukue no ue ni hon ga aru.","Ada buku di atas meja."),
    ("下","した/か","bawah","椅子の下を見て。","Isu no shita o mite.","Lihat di bawah kursi."),
    ("右","みぎ/う","kanan","右に曲がってください。","Migi ni magatte kudasai.","Tolong belok kanan."),
    ("左","ひだり/さ","kiri","左の手です。","Hidari no te desu.","Tangan kiri."),
    ("本","ほん/もと","buku","本を読みます。","Hon o yomimasu.","Membaca buku."),
    ("学","まなぶ/がく","belajar","学校で学びます。","Gakkou de manabimasu.","Belajar di sekolah."),
    ("先","さき/せん","duluan/guru","先生に聞きます。","Sensei ni kikimasu.","Bertanya kepada guru."),
    ("生","いきる/せい","hidup/lahir","元気に生きます。","Genki ni ikimasu.","Hidup dengan sehat."),
    ("年","とし/ねん","tahun","今年は何年ですか。","Kotoshi wa nannen desuka.","Tahun ini tahun berapa?"),
    ("食","たべる/しょく","makan","ご飯を食べます。","Gohan o tabemasu.","Makan nasi."),
    ("飲","のむ/いん","minum","水を飲みます。","Mizu o nomimasu.","Minum air."),
    ("見","みる/けん","melihat","テレビを見ます。","Terebi o mimasu.","Menonton TV."),
    ("聞","きく/ぶん","mendengar","音楽を聞きます。","Ongaku o kikimasu.","Mendengarkan musik."),
    ("書","かく/しょ","menulis","手紙を書きます。","Tegami o kakimasu.","Menulis surat."),
    ("読","よむ/どく","membaca","新聞を読みます。","Shinbun o yomimasu.","Membaca koran."),
    ("話","はなす/わ","berbicara","日本語で話します。","Nihongo de hanashimasu.","Berbicara dalam bahasa Jepang."),
    ("来","くる/らい","datang","友達が来ます。","Tomodachi ga kimasu.","Teman datang."),
    ("行","いく/こう","pergi","学校に行きます。","Gakkou ni ikimasu.","Pergi ke sekolah."),
    ("帰","かえる/き","pulang","家に帰ります。","Ie ni kaerimasu.","Pulang ke rumah."),
    ("白","しろ/はく","putih","白いシャツです。","Shiroi shatsu desu.","Kemeja putih."),
    ("黒","くろ/こく","hitam","黒い猫がいます。","Kuroi neko ga imasu.","Ada kucing hitam."),
    ("赤","あか/せき","merah","赤いリンゴです。","Akai ringo desu.","Apel merah."),
    ("青","あお/せい","biru","青い空がきれいです。","Aoi sora ga kirei desu.","Langit biru itu indah."),
    ("花","はな/か","bunga","花を買います。","Hana o kaimasu.","Membeli bunga."),
    ("雨","あめ/う","hujan","今日は雨です。","Kyou wa ame desu.","Hari ini hujan."),
    ("空","そら/くう","langit/kosong","空が青い。","Sora ga aoi.","Langit biru."),
    ("犬","いぬ/けん","anjing","犬が好きです。","Inu ga suki desu.","Suka anjing."),
    ("猫","ねこ/びょう","kucing","猫は可愛い。","Neko wa kawaii.","Kucing itu lucu."),
    ("魚","さかな/ぎょ","ikan","魚を食べます。","Sakana o tabemasu.","Makan ikan."),
    ("円","えん","yen/bulat","千円ください。","Senen kudasai.","Tolong beri 1000 yen."),
    ("気","き/け","perasaan/udara","元気ですか。","Genki desuka.","Apa kabar?"),
]

VOCAB = [
    ("おはようございます","Selamat pagi (formal)","おはようございます、先生！","Ohayou gozaimasu, sensei!","Selamat pagi, Sensei!"),
    ("こんにちは","Halo / Selamat siang","こんにちは、お元気ですか。","Konnichiwa, ogenki desuka.","Halo, apa kabar?"),
    ("こんばんは","Selamat malam","こんばんは、今日も疲れましたね。","Konbanwa, kyou mo tsukaremashita ne.","Selamat malam, hari ini juga lelah ya."),
    ("ありがとうございます","Terima kasih (formal)","助けてくれてありがとうございます。","Tasukete kurete arigatou gozaimasu.","Terima kasih sudah membantu."),
    ("すみません","Permisi / Maaf","すみません、駅はどこですか。","Sumimasen, eki wa doko desuka.","Permisi, di mana stasiunnya?"),
    ("はい","Ya","はい、わかりました。","Hai, wakarimashita.","Ya, saya mengerti."),
    ("いいえ","Tidak","いいえ、知りません。","Iie, shirimasen.","Tidak, saya tidak tahu."),
    ("わかりました","Mengerti / Paham","説明はわかりました。","Setsumei wa wakarimashita.","Penjelasannya sudah mengerti."),
    ("わかりません","Tidak mengerti","日本語がわかりません。","Nihongo ga wakarimasen.","Saya tidak mengerti bahasa Jepang."),
    ("どこ","Di mana","トイレはどこですか。","Toire wa doko desuka.","Di mana toilet?"),
    ("いつ","Kapan","授業はいつですか。","Jugyou wa itsu desuka.","Kapan kelasnya?"),
    ("だれ","Siapa","あの人は誰ですか。","Ano hito wa dare desuka.","Orang itu siapa?"),
    ("なに","Apa","それは何ですか。","Sore wa nan desuka.","Itu apa?"),
    ("いくら","Berapa harga","これはいくらですか。","Kore wa ikura desuka.","Ini berapa harganya?"),
    ("これ","Ini","これは私の本です。","Kore wa watashi no hon desu.","Ini buku saya."),
    ("それ","Itu","それは何ですか。","Sore wa nan desuka.","Itu apa?"),
    ("あれ","Itu (jauh)","あれは富士山です。","Are wa Fujisan desu.","Itu Gunung Fuji."),
    ("ここ","Di sini","ここに座ってください。","Koko ni suwatte kudasai.","Tolong duduk di sini."),
    ("そこ","Di sana","そこに鍵があります。","Soko ni kagi ga arimasu.","Kuncinya ada di sana."),
    ("いま","Sekarang","今何時ですか。","Ima nanji desuka.","Sekarang jam berapa?"),
    ("きょう","Hari ini","今日は何曜日ですか。","Kyou wa nanyoubi desuka.","Hari ini hari apa?"),
    ("あした","Besok","明日また会いましょう。","Ashita mata aimashou.","Sampai jumpa besok."),
    ("きのう","Kemarin","昨日は休みでした。","Kinou wa yasumi deshita.","Kemarin hari libur."),
    ("まいにち","Setiap hari","毎日日本語を勉強します。","Mainichi nihongo o benkyou shimasu.","Belajar bahasa Jepang setiap hari."),
    ("あさ","Pagi","朝ごはんを食べます。","Asa gohan o tabemasu.","Makan sarapan pagi."),
    ("よる","Malam","夜は早く寝ます。","Yoru wa hayaku nemasu.","Malam tidur cepat."),
    ("すき","Suka","ラーメンが好きです。","Raamen ga suki desu.","Saya suka ramen."),
    ("きらい","Tidak suka","虫が嫌いです。","Mushi ga kirai desu.","Saya tidak suka serangga."),
    ("おおきい","Besar","大きい家に住みたい。","Ookii ie ni sumitai.","Ingin tinggal di rumah besar."),
    ("ちいさい","Kecil","小さい犬が可愛い。","Chiisai inu ga kawaii.","Anjing kecil itu lucu."),
    ("たかい","Mahal/Tinggi","このレストランは高いです。","Kono resutoran wa takai desu.","Restoran ini mahal."),
    ("やすい","Murah","このお店は安いです。","Kono omise wa yasui desu.","Toko ini murah."),
    ("おいしい","Enak","このラーメンはおいしい！","Kono raamen wa oishii!","Ramen ini enak!"),
    ("むずかしい","Sulit","漢字は難しいです。","Kanji wa muzukashii desu.","Kanji itu sulit."),
    ("やさしい","Mudah/Baik hati","先生は優しいです。","Sensei wa yasashii desu.","Gurunya baik hati."),
    ("いきます","Pergi","学校に行きます。","Gakkou ni ikimasu.","Pergi ke sekolah."),
    ("きます","Datang","友達が来ます。","Tomodachi ga kimasu.","Teman datang."),
    ("たべます","Makan","寿司を食べます。","Sushi o tabemasu.","Makan sushi."),
    ("のみます","Minum","お茶を飲みます。","Ocha o nomimasu.","Minum teh."),
    ("みます","Melihat/Menonton","映画を見ます。","Eiga o mimasu.","Menonton film."),
    ("かきます","Menulis","名前を書きます。","Namae o kakimasu.","Menulis nama."),
    ("よみます","Membaca","本を読みます。","Hon o yomimasu.","Membaca buku."),
    ("はなします","Berbicara","電話で話します。","Denwa de hanashimasu.","Berbicara di telepon."),
    ("かいます","Membeli","スーパーで野菜を買います。","Suupaa de yasai o kaimasu.","Membeli sayuran di supermarket."),
    ("あります","Ada (benda)","財布がありますか。","Saifu ga arimasuka.","Apakah ada dompet?"),
    ("います","Ada (orang/hewan)","猫が家にいます。","Neko ga ie ni imasu.","Kucing ada di rumah."),
    ("でんしゃ","Kereta listrik","電車で行きます。","Densha de ikimasu.","Pergi naik kereta."),
    ("がっこう","Sekolah","学校は楽しいです。","Gakkou wa tanoshii desu.","Sekolah menyenangkan."),
    ("ともだち","Teman","友達と遊びます。","Tomodachi to asobimasu.","Bermain dengan teman."),
    ("かぞく","Keluarga","家族が大切です。","Kazoku ga taisetsu desu.","Keluarga itu penting."),
    ("せんせい","Guru","先生に質問します。","Sensei ni shitsumon shimasu.","Bertanya kepada guru."),
    ("べんきょう","Belajar","毎日勉強します。","Mainichi benkyou shimasu.","Belajar setiap hari."),
    ("にほんご","Bahasa Jepang","日本語は面白い。","Nihongo wa omoshiroi.","Bahasa Jepang itu menarik."),
    ("コーヒー","Kopi","朝コーヒーを飲みます。","Asa koohii o nomimasu.","Minum kopi di pagi hari."),
    ("ごはん","Nasi / Makanan","ご飯を食べましょう！","Gohan o tabemashou!","Ayo makan!"),
]

TIPS = [
    "Ulangi kanji sambil menulis — tangan membantu otak mengingat lebih lama!",
    "Baca kanji keras-keras saat belajar. Kombinasi visual + suara mempercepat hafalan.",
    "Coba buat kalimat sendiri menggunakan kanji hari ini. Kreativitas = ingatan kuat!",
    "Flashcard digital seperti Anki sangat efektif untuk kanji. Coba gunakan hari ini!",
    "Istirahat 5 menit setelah belajar 25 menit (Pomodoro). Otak butuh jeda untuk menyerap!",
    "Tulis kanji 5 kali sebelum tidur malam ini. Review sebelum tidur = ingatan lebih tajam.",
    "Konsistensi lebih penting dari intensitas. 10 menit setiap hari lebih baik dari 2 jam seminggu sekali.",
    "Hubungkan kanji baru dengan sesuatu yang sudah kamu tahu. Asosiasi = kunci hafalan!",
    "Jangan takut salah! Kesalahan adalah bagian terpenting dari proses belajar bahasa.",
    "Cari drama atau anime Jepang dengan subtitle. Mendengar langsung mempercepat pemahaman!",
]

def kirim_pesan(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

def pick_daily():
    today = datetime.now()
    seed = today.year * 10000 + today.month * 100 + today.day
    rng = random.Random(seed)
    return rng.sample(KANJI, 5), rng.sample(VOCAB, 5)

def buat_pesan():
    kanji_list, vocab_list = pick_daily()
    today = datetime.now()
    hari = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][today.weekday()]
    tanggal = today.strftime("%d %B %Y")
    tip = random.Random(today.year*10000+today.month*100+today.day+99).choice(TIPS)

    baris = []
    baris.append(f"🌸 *OHAYOU GOZAIMASU!* 🌸")
    baris.append(f"_{hari}, {tanggal}_")
    baris.append("Semangat belajar bahasa Jepang hari ini! ✨\n")
    baris.append("━━━━━━━━━━━━━━━━━━━━")
    baris.append("📖 *5 KANJI HARI INI*")
    baris.append("━━━━━━━━━━━━━━━━━━━━\n")
    for kanji, baca, arti, contoh, romaji, terjemah in kanji_list:
        baris.append(f"🔴 *{kanji}* — {baca}")
        baris.append(f"└ Arti: {arti}")
        baris.append(f"└ Contoh: {contoh}")
        baris.append(f"   ({romaji})")
        baris.append(f"   → {terjemah}\n")
    baris.append("━━━━━━━━━━━━━━━━━━━━")
    baris.append("💬 *5 KOSAKATA HARI INI*")
    baris.append("━━━━━━━━━━━━━━━━━━━━\n")
    for kata, arti, contoh, romaji, terjemah in vocab_list:
        baris.append(f"🔵 *{kata}* — {arti}")
        baris.append(f"└ Contoh: {contoh}")
        baris.append(f"   ({romaji})")
        baris.append(f"   → {terjemah}\n")
    baris.append("━━━━━━━━━━━━━━━━━━━━")
    baris.append(f"💪 *TIPS HARI INI*")
    baris.append(f"_{tip}_\n")
    baris.append("がんばってください！ 🎌")
    return "\n".join(baris)

def kirim_harian():
    log.info("Mengirim pesan harian...")
    try:
        kirim_pesan(buat_pesan())
        log.info("Pesan terkirim!")
    except Exception as e:
        log.error(f"Error: {e}")

async def main():
    log.info(f"Bot dimulai — jadwal: {HOUR:02d}:{MINUTE:02d} setiap hari")
    scheduler = AsyncIOScheduler(timezone="Asia/Tokyo")
    scheduler.add_job(kirim_harian, CronTrigger(hour=HOUR, minute=MINUTE, timezone="Asia/Tokyo"))
    scheduler.start()
    kirim_harian()
    while True:
        await asyncio.sleep(60)

asyncio.run(main())
