import os, json, random, logging, urllib.request
from datetime import datetime

TOKEN   = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

KANJI = [
    ("悲","かな/ひ","sedih","悲しい映画を見て泣いた。","Kanashii eiga o mite naita.","Menonton film sedih sampai menangis."),
    ("暑","あつ/しょ","panas (cuaca)","今日は本当に暑いですね。","Kyou wa hontou ni atsui desu ne.","Hari ini benar-benar panas ya."),
    ("寒","さむ/かん","dingin (cuaca)","冬は寒くて大変です。","Fuyu wa samukute taihen desu.","Musim dingin dingin sekali."),
    ("春","はる/しゅん","musim semi","春になると花が咲きます。","Haru ni naru to hana ga sakimasu.","Ketika musim semi tiba, bunga mekar."),
    ("夏","なつ/か","musim panas","夏休みに海へ行きます。","Natsuyasumi ni umi e ikimasu.","Pergi ke laut saat liburan musim panas."),
    ("秋","あき/しゅう","musim gugur","秋は紅葉がきれいです。","Aki wa kouyou ga kirei desu.","Musim gugur dedaunannya indah."),
    ("冬","ふゆ/とう","musim dingin","冬はスキーが楽しい。","Fuyu wa sukii ga tanoshii.","Musim dingin ski menyenangkan."),
    ("朝","あさ/ちょう","pagi","毎朝早く起きます。","Maiasa hayaku okimasu.","Bangun pagi setiap hari."),
    ("昼","ひる/ちゅう","siang","昼ごはんは何を食べますか。","Hirugohan wa nani o tabemasu ka.","Makan siang apa?"),
    ("夜","よる/や","malam","夜遅くまで勉強した。","Yoru osoku made benkyou shita.","Belajar sampai larut malam."),
    ("毎","まい","setiap","毎日日本語を練習します。","Mainichi nihongo o renshuu shimasu.","Berlatih bahasa Jepang setiap hari."),
    ("週","しゅう","minggu","来週テストがあります。","Raishuu tesuto ga arimasu.","Minggu depan ada ujian."),
    ("間","あいだ/かん","antara/selama","授業の間は静かにする。","Jugyou no aida wa shizuka ni suru.","Diam selama pelajaran."),
    ("前","まえ/ぜん","depan/sebelum","食事の前に手を洗う。","Shokuji no mae ni te o arau.","Cuci tangan sebelum makan."),
    ("後","あと/ご","belakang/setelah","授業の後で友達と話した。","Jugyou no ato de tomodachi to hanashita.","Berbicara dengan teman setelah kelas."),
    ("次","つぎ/じ","berikutnya","次の駅で降ります。","Tsugi no eki de orimasu.","Turun di stasiun berikutnya."),
    ("同","おな/どう","sama","同じ意見です。","Onaji iken desu.","Pendapat yang sama."),
    ("多","おお/た","banyak","宿題が多すぎる。","Shukudai ga oosugiru.","PR-nya terlalu banyak."),
    ("少","すこ/しょう","sedikit","少し待ってください。","Sukoshi matte kudasai.","Tolong tunggu sebentar."),
    ("長","なが/ちょう","panjang/lama","長い時間がかかった。","Nagai jikan ga kakatta.","Membutuhkan waktu yang lama."),
    ("短","みじか/たん","pendek/singkat","この映画は短い。","Kono eiga wa mijikai.","Film ini pendek."),
    ("高","たか/こう","tinggi/mahal","山が高い。","Yama ga takai.","Gunungnya tinggi."),
    ("低","ひく/てい","rendah","声が低い人です。","Koe ga hikui hito desu.","Orang yang suaranya rendah."),
    ("広","ひろ/こう","luas","公園が広いです。","Kouen ga hiroi desu.","Tamannya luas."),
    ("狭","せま/きょう","sempit","部屋が狭い。","Heya ga semai.","Kamarnya sempit."),
    ("強","つよ/きょう","kuat","強い風が吹いている。","Tsuyoi kaze ga fuite iru.","Angin kencang berhembus."),
    ("弱","よわ/じゃく","lemah","体が弱い人です。","Karada ga yowai hito desu.","Orang yang badannya lemah."),
    ("早","はや/そう","cepat/awal","早く起きてください。","Hayaku okite kudasai.","Tolong bangun cepat."),
    ("遅","おそ/ち","lambat/terlambat","電車が遅れています。","Densha ga okurete imasu.","Keretanya terlambat."),
    ("新","あたら/しん","baru","新しい仕事を始めた。","Atarashii shigoto o hajimeta.","Memulai pekerjaan baru."),
    ("古","ふる/こ","lama/tua","古い建物を修理した。","Furui tatemono o shuurishita.","Memperbaiki bangunan tua."),
    ("若","わか/じゃく","muda","若い人が増えている。","Wakai hito ga fuete iru.","Orang muda semakin bertambah."),
    ("太","ふと/た","gemuk/tebal","少し太ってしまった。","Sukoshi futotte shimatta.","Sedikit gemuk."),
    ("細","ほそ/さい","tipis/langsing","細い道を歩いた。","Hosoi michi o aruita.","Berjalan di jalan sempit."),
    ("重","おも/じゅう","berat","荷物が重い。","Nimotsu ga omoi.","Barang bawaannya berat."),
    ("軽","かる/けい","ringan","このバッグは軽い。","Kono baggu wa karui.","Tas ini ringan."),
    ("近","ちか/きん","dekat","駅が近くて便利です。","Eki ga chikakute benri desu.","Stasiunnya dekat, praktis."),
    ("遠","とお/えん","jauh","学校が家から遠い。","Gakkou ga ie kara tooi.","Sekolah jauh dari rumah."),
    ("明","あか/めい","terang/jelas","明るい部屋が好きです。","Akarui heya ga suki desu.","Suka kamar yang terang."),
    ("暗","くら/あん","gelap","急に暗くなった。","Kyuu ni kuraku natta.","Tiba-tiba menjadi gelap."),
    ("正","ただ/せい","benar/tepat","正しい答えを選んで。","Tadashii kotae o erande.","Pilih jawaban yang benar."),
    ("親","おや/しん","orang tua/akrab","親切にしてくれてありがとう。","Shinsetsu ni shite kurete arigatou.","Terima kasih sudah baik hati."),
    ("友","とも/ゆう","teman","友達と映画を見た。","Tomodachi to eiga o mita.","Menonton film bersama teman."),
    ("兄","あに/けい","kakak laki-laki","兄は医者です。","Ani wa isha desu.","Kakak laki-laki saya dokter."),
    ("姉","あね/し","kakak perempuan","姉は料理が上手です。","Ane wa ryouri ga jouzu desu.","Kakak perempuan pandai memasak."),
    ("弟","おとうと/てい","adik laki-laki","弟と一緒に遊んだ。","Otouto to issho ni asonda.","Bermain bersama adik laki-laki."),
    ("妹","いもうと/まい","adik perempuan","妹は学生です。","Imouto wa gakusei desu.","Adik perempuan saya pelajar."),
    ("夫","おっと/ふ","suami","夫は会社員です。","Otto wa kaishain desu.","Suami saya karyawan."),
    ("妻","つま/さい","istri","妻と一緒に料理します。","Tsuma to issho ni ryouri shimasu.","Memasak bersama istri."),
    ("体","からだ/たい","tubuh","体を大切にしてください。","Karada o taisetsu ni shite kudasai.","Tolong jaga tubuhmu."),
    ("頭","あたま/ず","kepala","頭が痛い。","Atama ga itai.","Kepala sakit."),
    ("顔","かお/がん","wajah","彼女は顔が可愛い。","Kanojo wa kao ga kawaii.","Wajahnya cantik."),
    ("声","こえ/せい","suara","大きな声で話してください。","Ookina koe de hanashite kudasai.","Tolong bicara dengan suara keras."),
    ("心","こころ/しん","hati/perasaan","心が温かい人です。","Kokoro ga atatakai hito desu.","Orang yang hatinya hangat."),
    ("力","ちから/りょく","kekuatan","力を合わせて頑張ろう。","Chikara o awasete ganbarou.","Mari berjuang dengan menyatukan kekuatan."),
    ("思","おも/し","berpikir/merasa","そう思います。","Sou omoimasu.","Saya pikir begitu."),
    ("考","かんが/こう","memikirkan","よく考えてから決める。","Yoku kangaete kara kimeru.","Memutuskan setelah berpikir matang."),
    ("感","かん","merasakan","感動しました。","Kandou shimashita.","Saya terharu."),
    ("言","い/げん","berkata","何も言わないでください。","Nani mo iwanaide kudasai.","Tolong jangan berkata apa-apa."),
    ("語","ご","bahasa/kata","日本語を勉強しています。","Nihongo o benkyou shite imasu.","Sedang belajar bahasa Jepang."),
    ("教","おし/きょう","mengajar","先生が数学を教えた。","Sensei ga suugaku o oshieta.","Guru mengajarkan matematika."),
    ("習","なら/しゅう","belajar/berlatih","ピアノを習っています。","Piano o naratte imasu.","Sedang belajar piano."),
    ("答","こた/とう","menjawab","質問に答えてください。","Shitsumon ni kotaete kudasai.","Tolong jawab pertanyaannya."),
    ("使","つか/し","menggunakan","辞書を使ってください。","Jisho o tsukatte kudasai.","Tolong gunakan kamus."),
    ("作","つく/さく","membuat","料理を作りました。","Ryouri o tsukurimashita.","Membuat masakan."),
    ("売","う/ばい","menjual","この店で野菜を売っている。","Kono mise de yasai o utte iru.","Toko ini menjual sayuran."),
    ("買","か/ばい","membeli","新しい本を買った。","Atarashii hon o katta.","Membeli buku baru."),
    ("借","か/しゃく","meminjam","図書館で本を借りた。","Toshokan de hon o karita.","Meminjam buku di perpustakaan."),
    ("貸","か/たい","meminjamkan","友達に傘を貸した。","Tomodachi ni kasa o kashita.","Meminjamkan payung kepada teman."),
    ("送","おく/そう","mengirim","メールを送りました。","Meeru o okurimashita.","Mengirim email."),
    ("着","き/ちゃく","tiba/memakai","駅に着きました。","Eki ni tsukimashita.","Sudah tiba di stasiun."),
    ("起","お/き","bangun/terjadi","事故が起きた。","Jiko ga okita.","Kecelakaan terjadi."),
    ("寝","ね/しん","tidur","早く寝てください。","Hayaku nete kudasai.","Tolong tidur cepat."),
    ("立","た/りつ","berdiri","立ってください。","Tatte kudasai.","Tolong berdiri."),
    ("座","すわ/ざ","duduk","どうぞ座ってください。","Douzo suwatte kudasai.","Silakan duduk."),
    ("走","はし/そう","berlari","公園を走った。","Kouen o hashitta.","Berlari di taman."),
    ("泳","およ/えい","berenang","海で泳いだ。","Umi de oyoida.","Berenang di laut."),
    ("飛","と/ひ","terbang","鳥が空を飛んでいる。","Tori ga sora o tonde iru.","Burung terbang di langit."),
    ("乗","の/じょう","menaiki","バスに乗ります。","Basu ni norimasu.","Naik bus."),
    ("降","お/こう","turun/hujan","電車を降りた。","Densha o orita.","Turun dari kereta."),
    ("開","あ/かい","membuka","窓を開けてください。","Mado o akete kudasai.","Tolong buka jendelanya."),
    ("閉","し/へい","menutup","ドアを閉めてください。","Doa o shimete kudasai.","Tolong tutup pintunya."),
    ("始","はじ/し","memulai","授業が始まります。","Jugyou ga hajimarimasu.","Pelajaran dimulai."),
    ("終","お/しゅう","mengakhiri","仕事が終わった。","Shigoto ga owatta.","Pekerjaan selesai."),
    ("止","と/し","berhenti","車が止まった。","Kuruma ga tomatta.","Mobil berhenti."),
    ("待","ま/たい","menunggu","少し待ってください。","Sukoshi matte kudasai.","Tolong tunggu sebentar."),
    ("会","あ/かい","bertemu","友達に会いました。","Tomodachi ni aimashita.","Bertemu dengan teman."),
    ("帰","かえ/き","pulang","家に帰ります。","Ie ni kaerimasu.","Pulang ke rumah."),
    ("出","で/しゅつ","keluar","家を出ました。","Ie o demashita.","Keluar dari rumah."),
    ("入","はい/にゅう","masuk","部屋に入ってください。","Heya ni haitte kudasai.","Tolong masuk ke kamar."),
    ("持","も/じ","membawa/memegang","傘を持って行く。","Kasa o motte iku.","Membawa payung pergi."),
    ("置","お/ち","meletakkan","机の上に置いた。","Tsukue no ue ni oita.","Meletakkan di atas meja."),
    ("切","き/せつ","memotong","紙を切った。","Kami o kitta.","Memotong kertas."),
    ("洗","あら/せん","mencuci","手を洗ってください。","Te o aratte kudasai.","Tolong cuci tangan."),
    ("脱","ぬ/だつ","melepas (pakaian)","靴を脱いでください。","Kutsu o nuide kudasai.","Tolong lepas sepatunya."),
    ("歌","うた/か","bernyanyi/lagu","歌を歌った。","Uta o utatta.","Menyanyikan lagu."),
    ("踊","おど/よう","menari","ダンスを踊った。","Dansu o odotta.","Menari dansa."),
    ("泣","な/きゅう","menangis","映画を見て泣いた。","Eiga o mite naita.","Menangis menonton film."),
    ("笑","わら/しょう","tertawa/senyum","友達と笑った。","Tomodachi to waratta.","Tertawa bersama teman."),
    ("怒","おこ/ど","marah","先生が怒った。","Sensei ga okotta.","Guru marah."),
    ("喜","よろこ/き","gembira","合格して喜んだ。","Goukaku shite yorokonda.","Gembira karena lulus."),
    ("忘","わす/ぼう","melupakan","名前を忘れた。","Namae o wasureta.","Lupa namanya."),
    ("覚","おぼ/かく","mengingat/menghafal","単語を覚えた。","Tango o oboeta.","Menghafal kosakata."),
    ("決","き/けつ","memutuskan","旅行の日程を決めた。","Ryokou no nittei o kimeta.","Memutuskan jadwal perjalanan."),
    ("選","えら/せん","memilih","プレゼントを選んだ。","Purezento o eranda.","Memilih hadiah."),
    ("変","か/へん","berubah","考えが変わった。","Kangae ga kawatta.","Pikiran berubah."),
    ("増","ふ/ぞう","bertambah","仕事が増えた。","Shigoto ga fueta.","Pekerjaan bertambah."),
    ("集","あつ/しゅう","mengumpulkan","情報を集めた。","Jouhou o atsumeta.","Mengumpulkan informasi."),
    ("助","たす/じょ","membantu","友達を助けた。","Tomodachi o tasuketa.","Membantu teman."),
    ("頼","たの/らい","meminta/mengandalkan","友達に頼んだ。","Tomodachi ni tanonda.","Meminta tolong teman."),
    ("信","しん","mempercayai","友達を信じる。","Tomodachi o shinjiru.","Mempercayai teman."),
    ("守","まも/しゅ","menjaga","ルールを守ってください。","Ruuru o mamotte kudasai.","Tolong patuhi aturan."),
    ("払","はら/ふつ","membayar","料金を払った。","Ryoukin o haratta.","Membayar biaya."),
    ("返","かえ/へん","mengembalikan","本を返した。","Hon o kaeshita.","Mengembalikan buku."),
    ("押","お/おう","mendorong","ボタンを押してください。","Botan o oshite kudasai.","Tolong tekan tombolnya."),
    ("引","ひ/いん","menarik","ドアを引いてください。","Doa o hiite kudasai.","Tolong tarik pintunya."),
    ("回","まわ/かい","berputar/kali","3回練習した。","Sankai renshuu shita.","Berlatih 3 kali."),
    ("落","お/らく","jatuh","財布が落ちた。","Saifu ga ochita.","Dompet jatuh."),
    ("建","た/けん","membangun","家を建てた。","Ie o tateta.","Membangun rumah."),
    ("住","す/じゅう","tinggal","東京に住んでいる。","Toukyou ni sunde iru.","Tinggal di Tokyo."),
    ("旅","たび/りょ","perjalanan","旅行が好きです。","Ryokou ga suki desu.","Suka berwisata."),
    ("泊","と/はく","menginap","ホテルに泊まった。","Hoteru ni tomatta.","Menginap di hotel."),
    ("遊","あそ/ゆう","bermain","公園で遊んだ。","Kouen de asonda.","Bermain di taman."),
    ("休","やす/きゅう","beristirahat","今日は休みます。","Kyou wa yasumimasu.","Hari ini istirahat."),
    ("働","はたら/どう","bekerja","毎日働いています。","Mainichi hataraite imasu.","Bekerja setiap hari."),
    ("練","れん","berlatih","毎日練習する。","Mainichi renshuu suru.","Berlatih setiap hari."),
    ("合","あ/ごう","cocok/lulus","試験に合格した。","Shiken ni goukaku shita.","Lulus ujian."),
    ("負","ま/ふ","kalah","試合に負けた。","Shiai ni maketa.","Kalah dalam pertandingan."),
    ("勝","か/しょう","menang","試合に勝った。","Shiai ni katta.","Menang dalam pertandingan."),
    ("似","に/じ","mirip","兄に似ています。","Ani ni nite imasu.","Mirip dengan kakak."),
    ("違","ちが/い","berbeda/salah","意見が違う。","Iken ga chigau.","Pendapat berbeda."),
]

VOCAB = [
    ("あいかわらず","seperti biasa/tidak berubah","相変わらず元気ですか。","Aikawarazu genki desuka.","Apakah kamu masih sehat seperti biasa?"),
    ("あげる","memberikan","友達にプレゼントをあげた。","Tomodachi ni purezento o ageta.","Memberi hadiah kepada teman."),
    ("あたりまえ","sudah sewajarnya","努力するのはあたりまえだ。","Doryoku suru no wa atarimae da.","Berusaha keras itu sudah sewajarnya."),
    ("あとで","nanti/setelah itu","あとで電話します。","Ato de denwa shimasu.","Nanti saya telepon."),
    ("いきなり","tiba-tiba/mendadak","いきなり雨が降ってきた。","Ikinari ame ga futte kita.","Tiba-tiba hujan turun."),
    ("いつのまにか","tanpa terasa/tahu-tahu","いつのまにか夜になった。","Itsu no ma ni ka yoru ni natta.","Tanpa terasa sudah malam."),
    ("うまい","enak/mahir","この料理はうまい。","Kono ryouri wa umai.","Masakan ini enak."),
    ("えんりょなく","tanpa sungkan","遠慮なく食べてください。","Enryo naku tabete kudasai.","Silakan makan tanpa sungkan."),
    ("おかえり","selamat datang (pulang)","おかえりなさい。","Okaerinasai.","Selamat datang kembali."),
    ("おかげさまで","berkat Anda/alhamdulillah","おかげさまで元気です。","Okagesama de genki desu.","Berkat Anda, saya sehat."),
    ("おじゃまします","permisi masuk ke rumah","おじゃまします。","Ojama shimasu.","Permisi, saya masuk ya."),
    ("おせわになる","mendapat bantuan","大変お世話になりました。","Taihen osewa ni narimashita.","Terima kasih banyak atas bantuan Anda."),
    ("おつかれさま","terima kasih sudah bekerja keras","お疲れ様でした。","Otsukare sama deshita.","Terima kasih sudah bekerja keras."),
    ("おもいきり","sekuat tenaga/sepuasnya","思い切り楽しんだ。","Omoikiri tanoshinda.","Bersenang-senang sepuasnya."),
    ("かえって","justru/malah","薬を飲んだらかえって悪くなった。","Kusuri o nondara kaette waruku natta.","Setelah minum obat justru semakin buruk."),
    ("かかる","membutuhkan (waktu/biaya)","時間がかかります。","Jikan ga kakarimasu.","Membutuhkan waktu."),
    ("かわりに","sebagai pengganti","私のかわりに行ってください。","Watashi no kawari ni itte kudasai.","Tolong pergi menggantikan saya."),
    ("きっと","pasti/tentu","きっとうまくいくよ。","Kitto umaku iku yo.","Pasti berhasil."),
    ("くれる","memberikan (kepada saya)","友達がプレゼントをくれた。","Tomodachi ga purezento o kureta.","Teman memberi saya hadiah."),
    ("こんなに","sebegini/seperti ini","こんなに難しいとは思わなかった。","Konna ni muzukashii to wa omowanakatta.","Tidak menyangka sesulit ini."),
    ("さっき","tadi/barusan","さっき電話がありました。","Sakki denwa ga arimashita.","Tadi ada telepon."),
    ("しかし","namun/tetapi","難しい。しかし諦めない。","Muzukashii. Shikashi akiramenai.","Sulit. Namun tidak menyerah."),
    ("じつは","sebenarnya","実は昨日行けなかった。","Jitsu wa kinou ikenakatta.","Sebenarnya kemarin tidak bisa pergi."),
    ("しばらく","sebentar/sementara waktu","しばらく待ってください。","Shibaraku matte kudasai.","Tolong tunggu sebentar."),
    ("じゃあ","kalau begitu","じゃあ、行きましょう。","Jaa, ikimashou.","Kalau begitu, mari pergi."),
    ("すっかり","sepenuhnya/benar-benar","すっかり忘れていた。","Sukkari wasurete ita.","Benar-benar sudah lupa."),
    ("せっかく","susah payah/khusus","せっかく来たのに会えなかった。","Sekkaku kita no ni aenakatta.","Sudah susah payah datang tapi tidak bisa bertemu."),
    ("そのうち","suatu saat nanti","そのうち慣れますよ。","Sono uchi naremasu yo.","Suatu saat nanti pasti terbiasa."),
    ("それに","selain itu/lagipula","安いし、それに美味しい。","Yasui shi, sore ni oishii.","Murah, lagipula enak."),
    ("そろそろ","sudah waktunya/sebentar lagi","そろそろ出発しましょう。","Sorosoro shuppatsu shimashou.","Sudah waktunya berangkat."),
    ("たしかに","memang benar/betul","確かにそうですね。","Tashika ni sou desu ne.","Memang benar begitu ya."),
    ("だいぶ","cukup banyak/lumayan","だいぶ上手になった。","Daibu jouzu ni natta.","Lumayan sudah mahir."),
    ("たまに","kadang-kadang/sesekali","たまに映画を見ます。","Tama ni eiga o mimasu.","Kadang-kadang menonton film."),
    ("だんだん","semakin lama semakin","だんだん寒くなってきた。","Dandan samuku natte kita.","Semakin lama semakin dingin."),
    ("ちゃんと","dengan benar/sungguh-sungguh","ちゃんと宿題をした。","Chanto shukudai o shita.","Mengerjakan PR dengan benar."),
    ("ついに","akhirnya","ついに目標を達成した。","Tsui ni mokuhyou o tassei shita.","Akhirnya mencapai tujuan."),
    ("つまり","artinya/dengan kata lain","つまり、無理だということです。","Tsumari, muri da to iu koto desu.","Artinya, itu tidak mungkin."),
    ("できるだけ","sebisa mungkin","できるだけ早く来てください。","Dekiru dake hayaku kite kudasai.","Tolong datang secepat mungkin."),
    ("とうとう","akhirnya/pada akhirnya","とうとう雨が降ってきた。","Toutou ame ga futte kita.","Akhirnya hujan turun juga."),
    ("ところで","ngomong-ngomong","ところで、昨日何をしましたか。","Tokoro de, kinou nani o shimashita ka.","Ngomong-ngomong, kemarin kamu ngapain?"),
    ("とにかく","pokoknya/bagaimanapun","とにかく頑張ろう。","Tonikaku ganbarou.","Pokoknya mari berjuang."),
    ("なぜ","mengapa","なぜ遅刻したのですか。","Naze chikoku shita no desuka.","Mengapa terlambat?"),
    ("はずだ","seharusnya","もう来るはずです。","Mou kuru hazu desu.","Seharusnya sudah datang."),
    ("はじめて","pertama kali","日本に初めて来た。","Nihon ni hajimete kita.","Pertama kali datang ke Jepang."),
    ("ばかり","hanya/baru saja","食べてばかりいる。","Tabete bakari iru.","Hanya makan saja terus."),
    ("ひさしぶり","lama tidak bertemu","久しぶりですね。","Hisashiburi desu ne.","Lama tidak bertemu ya."),
    ("まあまあ","lumayan/biasa saja","まあまあです。","Maa maa desu.","Lumayan."),
    ("まず","pertama-tama","まず手を洗ってください。","Mazu te o aratte kudasai.","Pertama-tama cuci tangan."),
    ("まるで","seolah-olah/bagaikan","まるで夢のようです。","Marude yume no you desu.","Seolah-olah seperti mimpi."),
    ("もしかしたら","mungkin saja","もしかしたら来ないかもしれない。","Moshikashitara konai kamo shirenai.","Mungkin saja tidak datang."),
    ("もちろん","tentu saja","もちろんいいですよ。","Mochiron ii desu yo.","Tentu saja boleh."),
    ("やはり","ternyata/memang","やはり難しかった。","Yahari muzukashikatta.","Ternyata memang sulit."),
    ("ようやく","akhirnya/baru saja bisa","ようやく終わった。","Youyaku owatta.","Akhirnya selesai."),
    ("よく","sering/dengan baik","よく分かりました。","Yoku wakarimashita.","Sudah betul-betul mengerti."),
    ("らしい","sepertinya/katanya","雨が降るらしい。","Ame ga furu rashii.","Sepertinya akan hujan."),
    ("わざと","dengan sengaja","わざとじゃないです。","Wazato ja nai desu.","Bukan dengan sengaja."),
    ("〜てあげる","melakukan untuk orang lain","荷物を持ってあげました。","Nimotsu o motte agemashita.","Membawakan barang untuk orang itu."),
    ("〜てもらう","meminta orang melakukan","説明してもらった。","Setsumei shite moratta.","Sudah dimintai penjelasan."),
    ("〜てくれる","orang melakukan untuk saya","手伝ってくれた。","Tetsudatte kureta.","Dibantu olehnya."),
    ("〜ておく","melakukan terlebih dahulu","準備しておいた。","Junbi shite oita.","Sudah bersiap terlebih dahulu."),
    ("〜てしまう","melakukan sampai selesai/menyesal","食べてしまった。","Tabete shimatta.","Sudah termakan semua."),
    ("〜てみる","mencoba melakukan","食べてみてください。","Tabete mite kudasai.","Coba dimakan."),
    ("〜ながら","sambil melakukan","音楽を聴きながら勉強した。","Ongaku o kiki nagara benkyou shita.","Belajar sambil mendengarkan musik."),
    ("〜ために","demi/untuk tujuan","健康のために運動する。","Kenkou no tame ni undou suru.","Olahraga demi kesehatan."),
    ("〜ように","agar supaya","忘れないようにメモした。","Wasurenai you ni memo shita.","Mencatat agar tidak lupa."),
    ("〜かもしれない","mungkin/bisa jadi","明日雨かもしれない。","Ashita ame kamo shirenai.","Besok mungkin hujan."),
    ("〜ばよかった","seandainya saja","もっと勉強すればよかった。","Motto benkyou sureba yokatta.","Seandainya saja belajar lebih giat."),
    ("〜でしょう","mungkin/sepertinya (dugaan)","明日は晴れでしょう。","Ashita wa hare deshou.","Besok mungkin cerah."),
    ("〜そうだ","kelihatannya/sepertinya akan","雨が降りそうです。","Ame ga furi sou desu.","Kelihatannya akan hujan."),
    ("〜すぎる","terlalu","食べすぎてしまった。","Tabesugite shimatta.","Terlalu banyak makan."),
    ("〜やすい","mudah untuk","この本は読みやすい。","Kono hon wa yomiyasui.","Buku ini mudah dibaca."),
    ("〜にくい","sulit untuk","この漢字は書きにくい。","Kono kanji wa kaki nikui.","Kanji ini sulit ditulis."),
    ("〜てから","setelah melakukan","宿題をしてから遊ぶ。","Shukudai o shite kara asobu.","Bermain setelah mengerjakan PR."),
    ("〜前に","sebelum","寝る前に歯を磨く。","Neru mae ni ha o migaku.","Menggosok gigi sebelum tidur."),
    ("〜まで","sampai/hingga","6時まで働いた。","Rokuji made hataraita.","Bekerja sampai jam 6."),
    ("〜について","tentang/mengenai","日本について話した。","Nihon ni tsuite hanashita.","Berbicara tentang Jepang."),
    ("〜のに","padahal/meskipun","頑張ったのに失敗した。","Ganbatta no ni shippai shita.","Padahal sudah berusaha, tapi gagal."),
    ("〜ても","meskipun/walaupun","雨でも行きます。","Ame demo ikimasu.","Meskipun hujan, tetap pergi."),
    ("〜たり〜たりする","melakukan ini itu bergantian","読んだり書いたりします。","Yondari kaitari shimasu.","Membaca atau menulis, dsb."),
    ("〜おかげで","berkat","先生のおかげで合格できた。","Sensei no okage de goukaku dekita.","Berkat guru, bisa lulus."),
    ("〜せいで","gara-gara","風邪のせいで休んだ。","Kaze no sei de yasunda.","Gara-gara flu, absen."),
    ("〜ほど〜ない","tidak se~ seperti","思ったほど難しくなかった。","Omotta hodo muzukashiku nakatta.","Tidak sesulit yang dibayangkan."),
    ("〜ばかりでなく","tidak hanya~ tapi juga","日本語ばかりでなく英語も話せる。","Nihongo bakari de naku eigo mo hanaseru.","Tidak hanya bahasa Jepang, bisa bahasa Inggris juga."),
]

TIPS = [
    "Kanji N4 banyak berhubungan dengan kehidupan sehari-hari — coba gunakan dalam percakapan!",
    "Pola kalimat 〜てあげる/もらう/くれる sangat sering dipakai. Hafalkan ketiganya!",
    "Coba tonton drama Jepang — banyak kosakata N4 muncul dalam percakapan natural.",
    "Belajar kanji N4 bersama on-yomi dan kun-yomi-nya sekaligus lebih efektif.",
    "Tulis 5 kalimat menggunakan kosakata hari ini — praktek langsung memperkuat ingatan!",
    "Spaced repetition adalah kunci. Review kata-kata lama sambil belajar yang baru.",
    "Baca teks bahasa Jepang sederhana setiap hari — manga untuk anak-anak cocok untuk N4.",
    "Konsistensi mengalahkan intensitas. 15 menit setiap hari lebih baik dari 3 jam seminggu.",
    "Jangan lewatkan pola 〜てしまう、〜ておく、〜てみる — ini kunci level N4!",
    "Coba catat kosakata baru dalam kalimat lengkap, bukan hanya kata tunggal.",
]

TOTAL_KANJI = len(KANJI)
TOTAL_VOCAB = len(VOCAB)
KANJI_PER_HARI = 5
VOCAB_PER_HARI = 5
TOTAL_HARI_KANJI = -(-TOTAL_KANJI // KANJI_PER_HARI)
TOTAL_HARI_VOCAB = -(-TOTAL_VOCAB // VOCAB_PER_HARI)
TOTAL_HARI = max(TOTAL_HARI_KANJI, TOTAL_HARI_VOCAB)

def kirim_pesan(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = json.dumps({"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req)

def get_hari_ke():
    # Hitung hari ke berapa sejak tanggal mulai (1 Juni 2026)
    mulai = datetime(2026, 6, 14)
    today = datetime.now()
    delta = (today - mulai).days
    return delta  # 0 = hari pertama, 1 = hari kedua, dst

def pick_hari_ini(hari_ke):
    # Ambil 5 kanji dan 5 vocab berdasarkan urutan hari
    kanji_start = (hari_ke * KANJI_PER_HARI) % TOTAL_KANJI
    vocab_start  = (hari_ke * VOCAB_PER_HARI) % TOTAL_VOCAB

    kanji_list = []
    for i in range(KANJI_PER_HARI):
        kanji_list.append(KANJI[(kanji_start + i) % TOTAL_KANJI])

    vocab_list = []
    for i in range(VOCAB_PER_HARI):
        vocab_list.append(VOCAB[(vocab_start + i) % TOTAL_VOCAB])

    return kanji_list, vocab_list

def cek_selesai(hari_ke):
    kanji_selesai = (hari_ke + 1) * KANJI_PER_HARI >= TOTAL_KANJI
    vocab_selesai = (hari_ke + 1) * VOCAB_PER_HARI >= TOTAL_VOCAB
    return kanji_selesai and vocab_selesai

def buat_pesan_selesai():
    msg = []
    msg.append("🎉 *SELAMAT! SEMUA MATERI N4 SELESAI!* 🎉\n")
    msg.append("━━━━━━━━━━━━━━━━━━━━")
    msg.append("🏆 *PENCAPAIAN LUAR BIASA!*")
    msg.append("━━━━━━━━━━━━━━━━━━━━\n")
    msg.append(f"✅ *{TOTAL_KANJI} Kanji N4* — Selesai dipelajari!")
    msg.append(f"✅ *{TOTAL_VOCAB} Kosakata N4* — Selesai dipelajari!\n")
    msg.append("Kamu telah menyelesaikan seluruh materi kanji dan")
    msg.append("kosakata level N4. Ini pencapaian yang luar biasa! 🌟\n")
    msg.append("━━━━━━━━━━━━━━━━━━━━")
    msg.append("📚 *LANGKAH SELANJUTNYA:*")
    msg.append("━━━━━━━━━━━━━━━━━━━━\n")
    msg.append("1️⃣ Review ulang dari awal untuk memperkuat ingatan")
    msg.append("2️⃣ Coba ikut ujian JLPT N4 resmi")
    msg.append("3️⃣ Mulai belajar materi N3 untuk level berikutnya\n")
    msg.append("━━━━━━━━━━━━━━━━━━━━")
    msg.append("🔄 *Bot akan mulai mengirim ulang dari awal besok.*\n")
    msg.append("おめでとうございます！ 🎌🎊")
    return "\n".join(msg)

def buat_pesan_harian(hari_ke, kanji_list, vocab_list):
    today = datetime.now()
    hari = ["Senin","Selasa","Rabu","Kamis","Jumat","Sabtu","Minggu"][today.weekday()]
    tanggal = today.strftime("%d %B %Y")
    tip = random.Random(today.year*10000+today.month*100+today.day+99).choice(TIPS)

    kanji_progress = min((hari_ke + 1) * KANJI_PER_HARI, TOTAL_KANJI)
    vocab_progress  = min((hari_ke + 1) * VOCAB_PER_HARI, TOTAL_VOCAB)

    baris = []
    baris.append("🌸 *OHAYOU GOZAIMASU!* 🌸")
    baris.append(f"_{hari}, {tanggal}_")
    baris.append(f"Hari ke-*{hari_ke + 1}* belajar bahasa Jepang N4! ✨\n")
    baris.append("━━━━━━━━━━━━━━━━━━━━")
    baris.append(f"📖 *5 KANJI N4 HARI INI* ({kanji_progress}/{TOTAL_KANJI})")
    baris.append("━━━━━━━━━━━━━━━━━━━━\n")
    for kanji, baca, arti, contoh, romaji, terjemah in kanji_list:
        baris.append(f"🔴 *{kanji}* — {baca}")
        baris.append(f"└ Arti: {arti}")
        baris.append(f"└ Contoh: {contoh}")
        baris.append(f"   ({romaji})")
        baris.append(f"   → {terjemah}\n")
    baris.append("━━━━━━━━━━━━━━━━━━━━")
    baris.append(f"💬 *5 KOSAKATA N4 HARI INI* ({vocab_progress}/{TOTAL_VOCAB})")
    baris.append("━━━━━━━━━━━━━━━━━━━━\n")
    for kata, arti, contoh, romaji, terjemah in vocab_list:
        baris.append(f"🔵 *{kata}* — {arti}")
        baris.append(f"└ Contoh: {contoh}")
        baris.append(f"   ({romaji})")
        baris.append(f"   → {terjemah}\n")
    baris.append("━━━━━━━━━━━━━━━━━━━━")
    baris.append("💪 *TIPS N4 HARI INI*")
    baris.append(f"_{tip}_\n")
    baris.append("がんばってください！ 🎌")
    return "\n".join(baris)

# === MAIN ===
hari_ke = get_hari_ke()
log.info(f"Hari ke-{hari_ke + 1} dari {TOTAL_HARI} hari")

kanji_list, vocab_list = pick_hari_ini(hari_ke)
pesan = buat_pesan_harian(hari_ke, kanji_list, vocab_list)
kirim_pesan(pesan)
log.info("Pesan harian terkirim!")

# Kirim notifikasi selesai jika hari ini adalah hari terakhir
if cek_selesai(hari_ke):
    kirim_pesan(buat_pesan_selesai())
    log.info("Notifikasi selesai terkirim!")

log.info("Selesai!")
