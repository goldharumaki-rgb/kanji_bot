import os, json, random, logging, urllib.request
from datetime import datetime

TOKEN   = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger(__name__)

KANJI = [
    ("悪","わる/あく","buruk/jahat","悪い天気が続いています。","Warui tenki ga tsuzuite imasu.","Cuaca buruk terus berlanjut."),
    ("安","やす/あん","murah/aman","この店は安くておいしい。","Kono mise wa yasukute oishii.","Toko ini murah dan enak."),
    ("暗","くら/あん","gelap","部屋が暗いので電気をつけた。","Heya ga kurai node denki o tsuketa.","Karena kamar gelap, saya nyalakan lampu."),
    ("医","い","dokter/mengobati","医者に診てもらった。","Isha ni mite moratta.","Saya diperiksa dokter."),
    ("育","そだ/いく","membesarkan/tumbuh","子どもを大切に育てる。","Kodomo o taisetsu ni sodateru.","Membesarkan anak dengan penuh kasih."),
    ("運","はこ/うん","nasib/mengangkut","運動は健康にいい。","Undou wa kenkou ni ii.","Olahraga baik untuk kesehatan."),
    ("映","うつ/えい","memantulkan/film","映画を見に行きました。","Eiga o mi ni ikimashita.","Saya pergi menonton film."),
    ("駅","えき","stasiun","駅まで歩いて10分です。","Eki made aruite juppun desu.","10 menit jalan kaki ke stasiun."),
    ("横","よこ/おう","samping/horisontal","横断歩道を渡ってください。","Oudanhodou o watatte kudasai.","Tolong seberangi zebra cross."),
    ("化","か/け","berubah/transformasi","文化の違いを理解する。","Bunka no chigai o rikai suru.","Memahami perbedaan budaya."),
    ("界","かい","dunia/batas","世界中を旅したい。","Sekaijuu o tabi shitai.","Ingin berkeliling dunia."),
    ("開","ひら/かい","membuka","会議を開きます。","Kaigi o hirakimasu.","Membuka rapat."),
    ("感","かん","perasaan/emosi","感謝の気持ちを伝えた。","Kansha no kimochi o tsutaeta.","Menyampaikan rasa terima kasih."),
    ("館","かん","gedung/bangunan","図書館で本を借りた。","Toshokan de hon o karita.","Meminjam buku di perpustakaan."),
    ("起","お/き","bangun/terjadi","毎朝6時に起きます。","Maiasa rokuji ni okimasu.","Bangun jam 6 setiap pagi."),
    ("急","いそ/きゅう","terburu-buru/mendadak","急いで駅に向かった。","Isoide eki ni mukatta.","Bergegas menuju stasiun."),
    ("去","さ/きょ","pergi/lalu","去年日本に行きました。","Kyonen Nihon ni ikimashita.","Tahun lalu pergi ke Jepang."),
    ("業","ぎょう/わざ","pekerjaan/industri","卒業式に出席した。","Sotsugyoushiki ni shusseki shita.","Menghadiri upacara kelulusan."),
    ("近","ちか/きん","dekat","駅の近くに住んでいます。","Eki no chikaku ni sunde imasu.","Tinggal dekat stasiun."),
    ("決","き/けつ","memutuskan","会議で決定しました。","Kaigi de kettei shimashita.","Diputuskan dalam rapat."),
    ("県","けん","prefektur","神奈川県に住んでいます。","Kanagawa-ken ni sunde imasu.","Tinggal di Prefektur Kanagawa."),
    ("験","けん","ujian/pengalaman","試験の結果が出た。","Shiken no kekka ga deta.","Hasil ujian sudah keluar."),
    ("功","こう","jasa/keberhasilan","成功するまで諦めない。","Seikou suru made akiramenai.","Tidak menyerah sampai berhasil."),
    ("港","みなと/こう","pelabuhan","神戸港は有名です。","Koube-kou wa yuumei desu.","Pelabuhan Kobe terkenal."),
    ("最","もっと/さい","paling/terbanyak","最高の結果を出した。","Saikou no kekka o dashita.","Menghasilkan hasil terbaik."),
    ("察","さつ","mengamati/memahami","状況を察して行動する。","Joukyou o sashite koudou suru.","Bertindak dengan memahami situasi."),
    ("産","う/さん","melahirkan/produk","地元の産物を大切にする。","Jimoto no sanbutsu o taisetsu ni suru.","Menghargai produk lokal."),
    ("試","こころ/し","mencoba/ujian","新しいことを試みる。","Atarashii koto o kokoromiru.","Mencoba hal baru."),
    ("治","なお/じ","menyembuhkan/memerintah","病気が治りました。","Byouki ga naorimashita.","Penyakitnya sudah sembuh."),
    ("守","まも/しゅ","menjaga/mematuhi","約束を守ってください。","Yakusoku o mamotte kudasai.","Tolong tepati janji."),
    ("受","う/じゅ","menerima","試験を受けます。","Shiken o ukemasu.","Mengikuti ujian."),
    ("集","あつ/しゅう","mengumpulkan","切手を集めています。","Kitte o atsumete imasu.","Saya mengoleksi perangko."),
    ("住","す/じゅう","tinggal","東京に住んでいます。","Toukyou ni sunde imasu.","Tinggal di Tokyo."),
    ("重","おも/じゅう","berat/penting","この荷物は重い。","Kono nimotsu wa omoi.","Barang bawaan ini berat."),
    ("所","ところ/しょ","tempat","好きな場所はどこですか。","Sukina basho wa doko desuka.","Di mana tempat favoritmu?"),
    ("助","たす/じょ","membantu/selamat","困っている人を助けた。","Komatte iru hito o tasuketa.","Membantu orang yang kesusahan."),
    ("乗","の/じょう","menaiki","電車に乗ります。","Densha ni norimasu.","Naik kereta."),
    ("身","み/しん","tubuh/diri","身体を大切にする。","Karada o taisetsu ni suru.","Menjaga tubuh dengan baik."),
    ("神","かみ/しん","dewa/Tuhan","神社にお参りした。","Jinja ni omairi shita.","Berziarah ke kuil Shinto."),
    ("進","すす/しん","maju/berkembang","計画が順調に進んでいる。","Keikaku ga junchou ni susunde iru.","Rencana berjalan dengan lancar."),
    ("親","おや/しん","orang tua/akrab","親に感謝する。","Oya ni kansha suru.","Berterima kasih kepada orang tua."),
    ("数","かず/すう","angka/jumlah","数学が得意です。","Suugaku ga tokui desu.","Saya pandai matematika."),
    ("制","せい","sistem/kontrol","制度を改善する。","Seido o kaizen suru.","Memperbaiki sistem."),
    ("席","せき","tempat duduk","席を予約しました。","Seki o yoyaku shimashita.","Memesan tempat duduk."),
    ("選","えら/せん","memilih","代表を選びます。","Daihyou o erabimasu.","Memilih perwakilan."),
    ("族","ぞく","kelompok/suku","家族旅行を計画した。","Kazoku ryokou o keikaku shita.","Merencanakan liburan keluarga."),
    ("続","つづ/ぞく","melanjutkan","練習を続けてください。","Renshuu o tsuzukete kudasai.","Tolong lanjutkan latihannya."),
    ("対","たい","melawan/pasangan","試合で対戦する。","Shiai de taisen suru.","Bertanding dalam pertandingan."),
    ("待","ま/たい","menunggu","バスを待っています。","Basu o matte imasu.","Sedang menunggu bus."),
    ("達","たち/たつ","mencapai/jamak orang","友達と出かけました。","Tomodachi to dekakemashita.","Pergi keluar bersama teman."),
    ("地","ち/じ","tanah/tempat","地図で確認する。","Chizu de kakunin suru.","Mengecek di peta."),
    ("知","し/ち","mengetahui","この情報を知っていますか。","Kono jouhou o shitte imasuka.","Apakah kamu tahu informasi ini?"),
    ("注","そそ/ちゅう","menuang/perhatian","注意してください。","Chuui shite kudasai.","Tolong perhatikan."),
    ("調","しら/ちょう","menyelidiki/nada","体調を整える。","Taichou o totonoeru.","Menjaga kondisi tubuh."),
    ("転","ころ/てん","berputar/pindah","自転車に乗る練習をした。","Jitensha ni noru renshuu o shita.","Berlatih naik sepeda."),
    ("都","みやこ/と","ibu kota/kota besar","東京都に住んでいます。","Toukyou-to ni sunde imasu.","Tinggal di Metropolis Tokyo."),
    ("動","うご/どう","bergerak","体を動かすことが大切だ。","Karada o ugokasu koto ga taisetsu da.","Menggerakkan tubuh itu penting."),
    ("農","のう","pertanian","農業を学んでいます。","Nougyou o manande imasu.","Sedang mempelajari pertanian."),
    ("配","くば/はい","mendistribusikan/khawatir","心配しないでください。","Shinpai shinaide kudasai.","Tolong jangan khawatir."),
    ("働","はたら/どう","bekerja","毎日一生懸命働いています。","Mainichi isshokenmei hataraite imasu.","Bekerja keras setiap hari."),
    ("発","はつ/ほつ","berangkat/mengeluarkan","新幹線が発車しました。","Shinkansen ga hassha shimashita.","Shinkansen sudah berangkat."),
    ("反","そ/はん","melawan/membalik","反対意見を述べた。","Hantai iken o nobeta.","Menyatakan pendapat yang menentang."),
    ("美","うつく/び","indah","美しい景色に感動した。","Utsukushii keshiki ni kandou shita.","Terpesona oleh pemandangan indah."),
    ("病","や/びょう","sakit/penyakit","病気で学校を休んだ。","Byouki de gakkou o yasunda.","Tidak masuk sekolah karena sakit."),
    ("部","ぶ","bagian/departemen","営業部に所属しています。","Eigyoubu ni shozoku shite imasu.","Saya tergabung di bagian penjualan."),
    ("服","ふく","pakaian","新しい服を買った。","Atarashii fuku o katta.","Membeli pakaian baru."),
    ("平","たい/へい","datar/damai","平和な世界を望む。","Heiwa na sekai o nozomu.","Mendambakan dunia yang damai."),
    ("別","わか/べつ","berpisah/berbeda","別の方法を試す。","Betsu no houhou o tamesu.","Mencoba cara yang berbeda."),
    ("法","ほう/のり","hukum/cara","方法を工夫する。","Houhou o kuufuu suru.","Memikirkan cara yang lebih baik."),
    ("望","のぞ/ぼう","berharap/memandang","成功を望んでいます。","Seikou o nozonde imasu.","Berharap untuk berhasil."),
    ("満","み/まん","penuh/puas","電車が満員です。","Densha ga man-in desu.","Kereta penuh sesak."),
    ("味","あじ/み","rasa/minat","この料理は味がいい。","Kono ryouri wa aji ga ii.","Masakan ini rasanya enak."),
    ("無","な/む","tidak ada/tanpa","無料で入れます。","Muryou de hairemasu.","Bisa masuk secara gratis."),
    ("命","いのち/めい","nyawa/perintah","命を大切にする。","Inochi o taisetsu ni suru.","Menghargai kehidupan."),
    ("問","と/もん","bertanya/masalah","問題を解決する。","Mondai o kaiketsu suru.","Menyelesaikan masalah."),
    ("役","やく","peran/berguna","役に立つ情報です。","Yaku ni tatsu jouhou desu.","Ini informasi yang berguna."),
    ("有","あ/ゆう","ada/memiliki","有名な場所を訪れた。","Yuumei na basho o otozureta.","Mengunjungi tempat yang terkenal."),
    ("予","あらかじ/よ","sebelumnya/rencana","予定を確認してください。","Yotei o kakunin shite kudasai.","Tolong cek jadwalnya."),
    ("落","お/らく","jatuh/santai","成績が落ちた。","Seiseki ga ochita.","Nilai turun."),
    ("利","き/り","keuntungan/tajam","便利な道具を使う。","Benri na dougu o tsukau.","Menggunakan alat yang praktis."),
    ("流","なが/りゅう","mengalir/aliran","川が静かに流れている。","Kawa ga shizuka ni nagarete iru.","Sungai mengalir dengan tenang."),
    ("旅","たび/りょ","perjalanan","旅行の計画を立てた。","Ryokou no keikaku o tateta.","Membuat rencana perjalanan."),
    ("和","なご/わ","harmoni/Jepang","和食が好きです。","Washoku ga suki desu.","Saya suka masakan Jepang."),
]

VOCAB = [
    ("あいさつ","salam/sapaan","毎朝あいさつをします。","Maiasa aisatsu o shimasu.","Memberi salam setiap pagi."),
    ("あきらめる","menyerah","夢をあきらめないで。","Yume o akiramenaide.","Jangan menyerah pada impianmu."),
    ("あつまる","berkumpul","みんなが公園に集まった。","Minna ga kouen ni atsumatta.","Semua berkumpul di taman."),
    ("あやまる","meminta maaf","失敗したのであやまった。","Shippai shita node ayamatta.","Meminta maaf karena gagal."),
    ("いつでも","kapan saja","いつでも相談してください。","Itsudemo soudan shite kudasai.","Silakan berkonsultasi kapan saja."),
    ("うける","menerima/mengikuti ujian","試験を受けます。","Shiken o ukemasu.","Mengikuti ujian."),
    ("うまくいく","berjalan dengan baik","計画がうまくいった。","Keikaku ga umaku itta.","Rencananya berjalan dengan baik."),
    ("えいきょう","pengaruh","天気が気分に影響する。","Tenki ga kibun ni eikyou suru.","Cuaca mempengaruhi suasana hati."),
    ("えんりょ","sungkan/menahan diri","遠慮しないでください。","Enryo shinaide kudasai.","Jangan sungkan."),
    ("おかげ","berkat/karena","あなたのおかげで助かった。","Anata no okage de tasukatta.","Terselamatkan berkat kamu."),
    ("おこなう","melaksanakan/melakukan","式典を行います。","Shikiten o okonaimasu.","Melaksanakan upacara."),
    ("おそらく","mungkin/kemungkinan besar","おそらく明日は雨でしょう。","Osoraku ashita wa ame deshou.","Kemungkinan besar besok akan hujan."),
    ("おたがい","satu sama lain","お互いに助け合いましょう。","Otagai ni tasuke aimashou.","Mari saling membantu satu sama lain."),
    ("おどろく","terkejut","その知らせに驚いた。","Sono shirase ni odoroita.","Terkejut dengan berita itu."),
    ("おもいやり","empati/perhatian","思いやりのある人が好きだ。","Omoiyari no aru hito ga suki da.","Suka orang yang penuh empati."),
    ("かいぎ","rapat","午後から会議があります。","Gogo kara kaigi ga arimasu.","Ada rapat dari siang."),
    ("かかわる","berhubungan/terlibat","この問題に関わっています。","Kono mondai ni kakawatte imasu.","Terlibat dalam masalah ini."),
    ("かくにん","konfirmasi/pengecekan","予約を確認してください。","Yoyaku o kakunin shite kudasai.","Tolong konfirmasi reservasinya."),
    ("かたづける","membereskan","部屋を片付けた。","Heya o katazuketa.","Membereskan kamar."),
    ("かならず","pasti/tentu","必ず時間を守ってください。","Kanarazu jikan o mamotte kudasai.","Tolong pasti tepat waktu."),
    ("かんがえかた","cara berpikir","考え方を変えてみよう。","Kangaekata o kaete miyou.","Mari mencoba mengubah cara berpikir."),
    ("かんきょう","lingkungan","環境を守ることが大切だ。","Kankyou o mamoru koto ga taisetsu da.","Menjaga lingkungan itu penting."),
    ("かんけい","hubungan/kaitan","この問題と関係がある。","Kono mondai to kankei ga aru.","Ada hubungannya dengan masalah ini."),
    ("かんしゃ","rasa syukur/terima kasih","感謝の気持ちを忘れない。","Kansha no kimochi o wasurenai.","Tidak melupakan rasa syukur."),
    ("かんじる","merasakan","春の暖かさを感じる。","Haru no atatakasa o kanjiru.","Merasakan hangatnya musim semi."),
    ("きけん","bahaya","危険な場所に近づかない。","Kiken na basho ni chikazukanai.","Tidak mendekati tempat berbahaya."),
    ("きびしい","keras/ketat","先生は厳しいが優しい。","Sensei wa kibishii ga yasashii.","Gurunya ketat tapi baik hati."),
    ("きまる","diputuskan/ditetapkan","日程が決まりました。","Nittei ga kimarimashita.","Jadwalnya sudah ditetapkan."),
    ("きゅうに","tiba-tiba","急に雨が降り始めた。","Kyuu ni ame ga furihajimeta.","Tiba-tiba hujan mulai turun."),
    ("きをつける","berhati-hati","車に気をつけてください。","Kuruma ni ki o tsukete kudasai.","Tolong berhati-hati dengan mobil."),
    ("くらべる","membandingkan","二つを比べてみた。","Futatsu o kurabete mita.","Mencoba membandingkan keduanya."),
    ("けいかく","rencana","旅行の計画を立てた。","Ryokou no keikaku o tateta.","Membuat rencana perjalanan."),
    ("けいけん","pengalaman","海外での経験が役立つ。","Kaigai de no keiken ga yakudatsu.","Pengalaman di luar negeri berguna."),
    ("けっか","hasil/akibat","努力の結果が出た。","Doryoku no kekka ga deta.","Hasil dari kerja keras sudah keluar."),
    ("けっして","sama sekali tidak","決して諦めません。","Kesshite akiramemasen.","Sama sekali tidak akan menyerah."),
    ("こうどう","tindakan/perilaku","積極的に行動する。","Sekkyokuteki ni koudou suru.","Bertindak secara aktif."),
    ("ことわる","menolak","誘いを断った。","Sasoi o kotowatta.","Menolak ajakan."),
    ("このごろ","belakangan ini","このごろ忙しいです。","Konogoro isogashii desu.","Belakangan ini sibuk."),
    ("さいきん","baru-baru ini","最近忙しくなった。","Saikin isogashiku natta.","Akhir-akhir ini semakin sibuk."),
    ("さいご","terakhir/akhir","最後まで頑張ってください。","Saigo made ganbatte kudasai.","Tolong semangat sampai akhir."),
    ("さらに","lebih lagi/selain itu","さらに詳しく説明します。","Sara ni kuwashiku setsumei shimasu.","Akan menjelaskan lebih detail lagi."),
    ("しかたがない","tidak bisa diapa-apakan","遅刻したのはしかたがない。","Chikoku shita no wa shikata ga nai.","Terlambat itu tidak bisa diapa-apakan."),
    ("しごと","pekerjaan","仕事が忙しい。","Shigoto ga isogashii.","Pekerjaan sedang sibuk."),
    ("しつれい","tidak sopan/permisi","失礼しました。","Shitsurei shimashita.","Maaf atas ketidaksopanan saya."),
    ("じっさい","kenyataannya/sebenarnya","実際に試してみた。","Jissai ni tameshite mita.","Mencoba dalam kenyataan."),
    ("じゅんび","persiapan","発表の準備をする。","Happyou no junbi o suru.","Mempersiapkan presentasi."),
    ("じょうほう","informasi","正確な情報が必要だ。","Seikaku na jouhou ga hitsuyou da.","Informasi yang akurat diperlukan."),
    ("しらべる","menyelidiki/mencari tahu","インターネットで調べた。","Intaanetto de shirabeta.","Mencari tahu di internet."),
    ("しんぱい","khawatir","心配しないでください。","Shinpai shinaide kudasai.","Jangan khawatir."),
    ("すすむ","maju/berkembang","勉強が順調に進んでいる。","Benkyou ga junchou ni susunde iru.","Belajar berjalan dengan lancar."),
    ("すっかり","sepenuhnya/sama sekali","すっかり忘れてしまった。","Sukkari wasurete shimatta.","Sudah benar-benar lupa."),
    ("せいかつ","kehidupan sehari-hari","健康的な生活を送る。","Kenkoukeki na seikatsu o okuru.","Menjalani kehidupan yang sehat."),
    ("ぜったいに","pasti/mutlak","絶対に諦めない。","Zettai ni akiramenai.","Pasti tidak akan menyerah."),
    ("そうだん","konsultasi","先生に相談した。","Sensei ni soudan shita.","Berkonsultasi dengan guru."),
    ("それほど","sebegitu/separah itu","それほど難しくない。","Sorehodo muzukashiku nai.","Tidak sesulit itu."),
    ("たいせつ","penting/berharga","家族は大切な存在だ。","Kazoku wa taisetsu na sonzai da.","Keluarga adalah keberadaan yang berharga."),
    ("たとえば","misalnya/contohnya","たとえば、りんごや桃などです。","Tatoeba, ringo ya momo nado desu.","Misalnya, apel atau persik dan sebagainya."),
    ("たのむ","meminta tolong/memesan","友達に手伝いを頼んだ。","Tomodachi ni tetsudai o tanonda.","Meminta tolong kepada teman."),
    ("ちがい","perbedaan","二つの意見の違いを説明する。","Futatsu no iken no chigai o setsumei suru.","Menjelaskan perbedaan dua pendapat."),
    ("ちょくせつ","langsung/secara langsung","直接話し合いました。","Chokusetsu hanashiaimashita.","Berdiskusi secara langsung."),
    ("つたえる","menyampaikan/memberitahu","大切なことを伝えたい。","Taisetsu na koto o tsutaetai.","Ingin menyampaikan hal penting."),
    ("つづける","melanjutkan/meneruskan","毎日練習を続ける。","Mainichi renshuu o tsuzukeru.","Melanjutkan latihan setiap hari."),
    ("てつだう","membantu/menolong","引越しを手伝いました。","Hikkoshi o tetsudaimashita.","Membantu pindahan."),
    ("とくに","terutama/khususnya","特に数学が得意です。","Toku ni suugaku ga tokui desu.","Terutama pandai matematika."),
    ("なかなか","cukup/lumayan/tidak mudah","なかなか難しい問題だ。","Nakanaka muzukashii mondai da.","Ini masalah yang cukup sulit."),
    ("なるべく","sebisa mungkin","なるべく早く来てください。","Narubeku hayaku kite kudasai.","Tolong datang secepat mungkin."),
    ("にがて","tidak pandai/lemah dalam","数学が苦手です。","Suugaku ga nigate desu.","Tidak pandai matematika."),
    ("はっきり","dengan jelas/tegas","はっきり言ってください。","Hakkiri itte kudasai.","Tolong bicara dengan jelas."),
    ("はなしあう","berdiskusi/berunding","問題について話し合った。","Mondai ni tsuite hanashiatta.","Berdiskusi tentang masalah."),
    ("はんたい","kebalikan/menentang","計画に反対する人がいる。","Keikaku ni hantai suru hito ga iru.","Ada orang yang menentang rencana."),
    ("ひつよう","perlu/diperlukan","パスポートが必要です。","Pasupooto ga hitsuyou desu.","Paspor diperlukan."),
    ("ふつう","biasa/normal","普通に生活しています。","Futsuu ni seikatsu shite imasu.","Menjalani kehidupan yang normal."),
    ("ぶんか","budaya","日本の文化に興味がある。","Nihon no bunka ni kyoumi ga aru.","Tertarik dengan budaya Jepang."),
    ("へんか","perubahan","気候の変化が激しい。","Kikou no henka ga hageshii.","Perubahan iklim sangat drastis."),
    ("ほうほう","cara/metode","効率的な方法を探す。","Kouritsutek na houhou o sagasu.","Mencari cara yang efisien."),
    ("まにあう","tepat waktu/keburu","電車に間に合った。","Densha ni ma ni atta.","Keburu keretanya."),
    ("まもる","menjaga/melindungi","環境を守る必要がある。","Kankyou o mamoru hitsuyou ga aru.","Perlu menjaga lingkungan."),
    ("むしろ","lebih baik/justru","むしろ一人の方が楽だ。","Mushiro hitori no hou ga raku da.","Justru lebih nyaman sendirian."),
    ("もったいない","sayang/mubazir","食べ物を捨てるのはもったいない。","Tabemono o suteru no wa mottainai.","Sayang membuang makanan."),
    ("やくにたつ","berguna/bermanfaat","この知識はきっと役に立つ。","Kono chishiki wa kitto yaku ni tatsu.","Pengetahuan ini pasti berguna."),
    ("やっぱり","ternyata/memang","やっぱり日本語は難しい。","Yappari nihongo wa muzukashii.","Ternyata bahasa Jepang memang sulit."),
    ("ゆっくり","pelan-pelan/santai","ゆっくり話してください。","Yukkuri hanashite kudasai.","Tolong bicara pelan-pelan."),
    ("よてい","jadwal/rencana","明日の予定は何ですか。","Ashita no yotei wa nan desuka.","Apa rencanamu besok?"),
    ("りかい","pemahaman/pengertian","相手の気持ちを理解する。","Aite no kimochi o rikai suru.","Memahami perasaan orang lain."),
    ("りゆう","alasan/sebab","遅刻した理由を説明した。","Chikoku shita riyuu o setsumei shita.","Menjelaskan alasan terlambat."),
    ("れんしゅう","latihan/praktik","毎日練習することが大切だ。","Mainichi renshuu suru koto ga taisetsu da.","Berlatih setiap hari itu penting."),
    ("れんらく","kontak/pemberitahuan","明日連絡します。","Ashita renraku shimasu.","Saya akan menghubungi besok."),
    ("わざわざ","sengaja/repot-repot","わざわざ来てくれてありがとう。","Wazawaza kite kurete arigatou.","Terima kasih sudah repot-repot datang."),
]

TIPS = [
    "Kanji N3 lebih kompleks — fokus pada radical untuk membantu hafalan!",
    "Buat kalimat sendiri dengan kosakata N3 hari ini. Konteks nyata = ingatan lebih kuat!",
    "Coba baca berita Jepang sederhana di NHK Web Easy — cocok untuk level N3.",
    "Pelajari pola kalimat N3 seperti 〜ために、〜ように、〜ながら secara bertahap.",
    "Review kanji yang sudah dipelajari seminggu lalu. Spaced repetition = kunci sukses!",
    "Tulis diary singkat dalam bahasa Jepang menggunakan kosakata hari ini.",
    "Konsistensi adalah kunci. Belajar 20 menit setiap hari lebih baik dari 3 jam seminggu sekali.",
    "Pahami nuansa kata — misalnya perbedaan むしろ vs かえって sangat penting di N3!",
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
    baris.append("🌸 *OHAYOU GOZAIMASU!* 🌸")
    baris.append(f"_{hari}, {tanggal}_")
    baris.append("Semangat belajar bahasa Jepang N3 hari ini! ✨\n")
    baris.append("━━━━━━━━━━━━━━━━━━━━")
    baris.append("📖 *5 KANJI N3 HARI INI*")
    baris.append("━━━━━━━━━━━━━━━━━━━━\n")
    for kanji, baca, arti, contoh, romaji, terjemah in kanji_list:
        baris.append(f"🔴 *{kanji}* — {baca}")
        baris.append(f"└ Arti: {arti}")
        baris.append(f"└ Contoh: {contoh}")
        baris.append(f"   ({romaji})")
        baris.append(f"   → {terjemah}\n")
    baris.append("━━━━━━━━━━━━━━━━━━━━")
    baris.append("💬 *5 KOSAKATA N3 HARI INI*")
    baris.append("━━━━━━━━━━━━━━━━━━━━\n")
    for kata, arti, contoh, romaji, terjemah in vocab_list:
        baris.append(f"🔵 *{kata}* — {arti}")
        baris.append(f"└ Contoh: {contoh}")
        baris.append(f"   ({romaji})")
        baris.append(f"   → {terjemah}\n")
    baris.append("━━━━━━━━━━━━━━━━━━━━")
    baris.append("💪 *TIPS N3 HARI INI*")
    baris.append(f"_{tip}_\n")
    baris.append("がんばってください！ 🎌")
    return "\n".join(baris)

log.info("Mengirim pesan harian N3...")
kirim_pesan(buat_pesan())
log.info("Selesai!")
