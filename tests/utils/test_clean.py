import unittest
from ccquery.utils import str_utils

class TestCleanup(unittest.TestCase):
    """Test the string cleanup methods"""

    def setUp(self):
        """Set up various clean or erroneous string formats"""

        self.examples = [
            '12 334 423523 543534',
            'witcher 3 enhanced edition',
            'excel deplacement flèche clavier',
            "de littérature et d'eau fraiche a blanchard",
            'apollo 8, apollo 8p, apollo 16 thomann',
            'croisière norvege juin 2018',
            'log4j threshold',
            'lecteur samsun bd-d8500-zf',
            "roue tvingo 14''occasion",
            '1-jour-1-question salomo',
            "distace saint-jean-d'arvey toulon",
            'iphone 4s',
            'app2sd',
            'moulin;com',
            '5google',
            'tech-zoo.com',
            'aplimo 2000w',
            'renault 4.5 tonnes',
            'vcredist x86 2011',
            't430 vs t430s vs t430',
            '67/69 rue aristide briand',
            '94440 villecresnes',
            'kabel deutschlan id 00000000000000f3',
            'access violation at adress 000000',
            'name of the langauage correspondinf to 040c:0000040c',
            'd&chetterie thyez horaires',
            's.e.l.a.r.l. clotilde griffon huissier',
            'con-e-co electric engine concrete mxier in portugal',
            'geogebra comparaison ilegale x<-0.25',
            '*thierry compte* billon sa',
            '!tenchy!?',
            'a!azon',
            'streeaming rrrrrrr!!!',
            'p!nk beautfiul trauma',
            "'!g rilettes thon persil'",
            'f!èvre jaune brésil salvador',
            'pakman jeux!!!!!!!!!!!!!!!',
            'à samedi !” roman graphiqu',
            '!!!!!!!!!!!!!tracteurs vido',
            'seloger?.com',
            'leclerc rouffiac loca†ion camion',
            'des rẑeves sans etoiles',
            'recette tarte pẑte brisée pur  eurre',
            'kã©mi seba',
            'землетрясение 2016 ford',
            "!! samsung galaxy tab a3ne s'allumeplus que faire ?",
            '最終痴漢電車 walkthrough',
            '木刀 teaduire en français',
            'テクノアーツ目黒区',
            '☀️ kss kss... zzzzt...',
            '""th�me:strasa - mono"" wwwbf com',
            'casque blutouth r�ducteur de bruit',
            'famine  en afrique  subsha�rienne',
            "rapport«mission monnaies locales complémentaires»",
            "première partieavril 2015p.29/76sylvio   gesel",
            'calucler temp après chauffe j/(kg°c)',
            '¢£¤§¨©«­®°²³´µ·¹º»¼½¿É×ßàáâãäåæçèéêëìíîïñòóôö÷øùúûüýþÿăćĉďđē',
            '¢£¤§¨©«­®°²³´µ·¹º»¼½¿ É ßàáâãäåæçèéêëìíîïñòóôö ÷ øùúûüýþÿăćĉďđē',
            'ėğĥīıĺľłńőœŕŝşšţźɔəʊʼˋ˜̧̀́̂̈έαγδεηθικλμνξοπρςστυωώвийкортцابةتجدرسع',
            'ėğĥīıĺľłńőœŕŝşšţźɔəʊ ʼˋ˜ έαγδεηθικλμνξοπρςστυωώвийкортцابةتجدرسع',
            'فقكلمهيẑếễỏ‐‑–—‘’‚‟†•…‬‹⁄ⁿ₁€™−√≠▒►☀。イウエガクコジプホムレンー三不与',
            'فقكلمهي ẑếễỏ ‐‑–—‘’‚‟†•…‬‹⁄ⁿ₁€™−√≠▒►☀。イウエガクコジプホムレンー三不与',
            '世了儿兼凡刀到可安平得掌晚木毛波海清熊猫界的认郭鱼默꼭바숨질ﬂ️﻿，�',
            '世了儿兼凡刀到可安平得掌晚木毛波海清熊猫界的认郭鱼默꼭바숨질 ﬂ ️﻿， �',
        ]

    def test_clean_text(self):
        ref_examples = [
            '12 334 423523 543534',
            'witcher 3 enhanced edition',
            'excel deplacement flèche clavier',
            "de littérature et d' eau fraiche a blanchard",
            'apollo 8, apollo 8p, apollo 16 thomann',
            'croisière norvege juin 2018',
            'log4j threshold',
            'lecteur samsun bd-d8500-zf',
            "roue tvingo 14'' occasion",
            '1-jour-1-question salomo',
            "distace saint-jean-d' arvey toulon",
            'iphone 4s',
            'app2sd',
            'moulin;com',
            '5google',
            'tech-zoo.com',
            'aplimo 2000w',
            'renault 4.5 tonnes',
            'vcredist x86 2011',
            't430 vs t430s vs t430',
            '67/69 rue aristide briand',
            '94440 villecresnes',
            'kabel deutschlan id 00000000000000f3',
            'access violation at adress 000000',
            'name of the langauage correspondinf to 040c:0000040c',
            'd&chetterie thyez horaires',
            's.e.l.a.r.l. clotilde griffon huissier',
            'con-e-co electric engine concrete mxier in portugal',
            'geogebra comparaison ilegale x<-0.25',
            '*thierry compte* billon sa',
            '!tenchy!?',
            'a!azon',
            'streeaming rrrrrrr!!!',
            'p!nk beautfiul trauma',
            "' !g rilettes thon persil'",
            'f!èvre jaune brésil salvador',
            'pakman jeux!!!!!!!!!!!!!!!',
            'à samedi !” roman graphiqu',
            '!!!!!!!!!!!!!tracteurs vido',
            'seloger?.com',
            'leclerc rouffiac loca†ion camion',
            'des rẑeves sans etoiles',
            'recette tarte pẑte brisée pur eurre',
            'seba',
            '2016 ford',
            "!! samsung galaxy tab a3ne s' allumeplus que faire ?",
            'walkthrough',
            'teaduire en français',
            '',
            'kss kss... zzzzt...',
            '""th�me:strasa - mono"" wwwbf com',
            'casque blutouth r�ducteur de bruit',
            'famine en afrique subsha�rienne',
            "rapport«mission monnaies locales complémentaires»",
            "première partieavril gesel",
            'calucler temp après chauffe',
            '',
            'é ßàáâãäåæçèéêëìíîïñòóôö øùúûüýþÿăćĉďđē',
            '',
            'ėğĥīıĺľłńőœŕŝşšţźɔəʊ',
            '',
            'ẑếễỏ',
            '',
            'ﬂ �',
        ]

        cleaned_examples = [
            str_utils.clean_text(text, 'LATIN')
            for text in self.examples]

        self.assertEqual(ref_examples, cleaned_examples)

    def test_clean_punctuation(self):
        ref_examples = [
            '',
            'witcher enhanced edition',
            'excel deplacement flèche clavier',
            "de littérature et d' eau fraiche a blanchard",
            'apollo apollo p apollo thomann',
            'croisière norvege juin',
            'log j threshold',
            'lecteur samsun bd d zf',
            "roue tvingo '' occasion",
            'jour question salomo',
            "distace saint jean d' arvey toulon",
            'iphone s',
            'app sd',
            'moulin com',
            'google',
            'tech zoo com',
            'aplimo w',
            'renault tonnes',
            'vcredist x',
            't vs t s vs t',
            'rue aristide briand',
            'villecresnes',
            'kabel deutschlan id f',
            'access violation at adress',
            'name of the langauage correspondinf to c c',
            'd chetterie thyez horaires',
            's e l a r l clotilde griffon huissier',
            'con e co electric engine concrete mxier in portugal',
            'geogebra comparaison ilegale x',
            'thierry compte billon sa',
            'tenchy',
            'a azon',
            'streeaming rrrrrrr',
            'p nk beautfiul trauma',
            "' g rilettes thon persil'",
            'f èvre jaune brésil salvador',
            'pakman jeux',
            'à samedi roman graphiqu',
            'tracteurs vido',
            'seloger com',
            'leclerc rouffiac loca ion camion',
            'des rẑeves sans etoiles',
            'recette tarte pẑte brisée pur eurre',
            'kã mi seba',
            'ford',
            "samsung galaxy tab a ne s' allumeplus que faire",
            'walkthrough',
            'teaduire en français',
            '',
            'kss kss zzzzt',
            'th me strasa mono wwwbf com',
            'casque blutouth r ducteur de bruit',
            'famine en afrique subsha rienne',
            "rapport mission monnaies locales complémentaires",
            "première partieavril p sylvio gesel",
            'calucler temp après chauffe j kg c',
            'é ßàáâãäåæçèéêëìíîïñòóôö øùúûüýþÿăćĉďđē',
            'é ßàáâãäåæçèéêëìíîïñòóôö øùúûüýþÿăćĉďđē',
            'ėğĥīıĺľłńőœŕŝşšţźɔəʊ',
            'ėğĥīıĺľłńőœŕŝşšţźɔəʊ',
            'ẑếễỏ',
            'ẑếễỏ',
            'ﬂ',
            'ﬂ',
        ]

        cleaned_examples = [
            str_utils.clean_text(text, 'LATIN', ignore_punctuation='noise-a')
            for text in self.examples]

        self.assertEqual(ref_examples, cleaned_examples)

    def test_define_words(self):
        ref_examples = [
            [],
            ['witcher', 'enhanced', 'edition'],
            ['excel', 'deplacement', 'flèche', 'clavier'],
            ['de', 'littérature', 'et', "d'eau", 'fraiche', 'a', 'blanchard'],
            ['apollo', 'apollo', 'p', 'apollo', 'thomann'],
            ['croisière', 'norvege', 'juin'],
            ['log', 'j', 'threshold'],
            ['lecteur', 'samsun', 'bd', 'd', 'zf'],
            ['roue', 'tvingo', 'occasion'],
            ['jour', 'question', 'salomo'],
            ['distace', 'saint', 'jean', "d'arvey", 'toulon'],
            ['iphone', 's'],
            ['app', 'sd'],
            ['moulin', 'com'],
            ['google'],
            ['tech', 'zoo', 'com'],
            ['aplimo', 'w'],
            ['renault', 'tonnes'],
            ['vcredist', 'x'],
            ['t', 'vs', 't', 's', 'vs', 't'],
            ['rue', 'aristide', 'briand'],
            ['villecresnes'],
            ['kabel', 'deutschlan', 'id', 'f'],
            ['access', 'violation', 'at', 'adress'],
            ['name', 'of', 'the', 'langauage', 'correspondinf', 'to', 'c', 'c'],
            ['d', 'chetterie', 'thyez', 'horaires'],
            ['s', 'e', 'l', 'a', 'r', 'l', 'clotilde', 'griffon', 'huissier'],
            ['con', 'e', 'co', 'electric', 'engine', 'concrete', 'mxier', 'in',
            'portugal'],
            ['geogebra', 'comparaison', 'ilegale', 'x'],
            ['thierry', 'compte', 'billon', 'sa'],
            ['tenchy'],
            ['a', 'azon'],
            ['streeaming', 'rrrrrrr'],
            ['p', 'nk', 'beautfiul', 'trauma'],
            ['g', 'rilettes', 'thon', 'persil'],
            ['f', 'èvre', 'jaune', 'brésil', 'salvador'],
            ['pakman', 'jeux'],
            ['à', 'samedi', 'roman', 'graphiqu'],
            ['tracteurs', 'vido'],
            ['seloger', 'com'],
            ['leclerc', 'rouffiac', 'loca', 'ion', 'camion'],
            ['des', 'rẑeves', 'sans', 'etoiles'],
            ['recette', 'tarte', 'pẑte', 'brisée', 'pur', 'eurre'],
            ['kã', 'mi', 'seba'],
            ['ford'],
            ['samsung', 'galaxy', 'tab', 'a', 'ne', "s'allumeplus", 'que',
            'faire'],
            ['walkthrough'],
            ['teaduire', 'en', 'français'],
            [],
            ['kss', 'kss', 'zzzzt'],
            ['th', 'me', 'strasa', 'mono', 'wwwbf', 'com'],
            ['casque', 'blutouth', 'r', 'ducteur', 'de', 'bruit'],
            ['famine', 'en', 'afrique', 'subsha', 'rienne'],
            ['rapport', 'mission', 'monnaies', 'locales', 'complémentaires'],
            ['première', 'partieavril', 'p', 'sylvio', 'gesel'],
            ['calucler', 'temp', 'après', 'chauffe', 'j', 'kg', 'c'],
            ['é', 'ßàáâãäåæçèéêëìíîïñòóôö', 'øùúûüýþÿăćĉďđē'],
            ['é', 'ßàáâãäåæçèéêëìíîïñòóôö', 'øùúûüýþÿăćĉďđē'],
            ['ėğĥīıĺľłńőœŕŝşšţźɔəʊ'],
            ['ėğĥīıĺľłńőœŕŝşšţźɔəʊ'],
            ['ẑếễỏ'],
            ['ẑếễỏ'],
            ['ﬂ'],
            ['ﬂ'],
        ]

        cleaned_examples = [
            str_utils.get_words(text, 'LATIN')
            for text in self.examples]

        self.assertEqual(ref_examples, cleaned_examples)

    def test_define_sentences(self):
        ref_examples = [
            ['12 334 423523 543534'],
            ['witcher 3 enhanced edition'],
            ['excel deplacement flèche clavier'],
            ["de littérature et d'eau fraiche a blanchard"],
            ['apollo 8, apollo 8p, apollo 16 thomann'],
            ['croisière norvege juin 2018'],
            ['log4j threshold'],
            ['lecteur samsun bd-d8500-zf'],
            ["roue tvingo 14''occasion"],
            ['1-jour-1-question salomo'],
            ["distace saint-jean-d'arvey toulon"],
            ['iphone 4s'],
            ['app2sd'],
            ['moulin;com'],
            ['5google'],
            ['tech-zoo', 'com'],
            ['aplimo 2000w'],
            ['renault 4', '5 tonnes'],
            ['vcredist x86 2011'],
            ['t430 vs t430s vs t430'],
            ['67/69 rue aristide briand'],
            ['94440 villecresnes'],
            ['kabel deutschlan id 00000000000000f3'],
            ['access violation at adress 000000'],
            ['name of the langauage correspondinf to 040c:0000040c'],
            ['d&chetterie thyez horaires'],
            ['s', 'e', 'l', 'a', 'r', 'l', 'clotilde griffon huissier'],
            ['con-e-co electric engine concrete mxier in portugal'],
            ['geogebra comparaison ilegale x<-0', '25'],
            ['*thierry compte* billon sa'],
            ['tenchy'],
            ['a', 'azon'],
            ['streeaming rrrrrrr'],
            ['p', 'nk beautfiul trauma'],
            ["'", "g rilettes thon persil'"],
            ['f', 'èvre jaune brésil salvador'],
            ['pakman jeux'],
            ['à samedi', '” roman graphiqu'],
            ['tracteurs vido'],
            ['seloger', 'com'],
            ['leclerc rouffiac loca†ion camion'],
            ['des rẑeves sans etoiles'],
            ['recette tarte pẑte brisée pur  eurre'],
            ['kã©mi seba'],
            ['землетрясение 2016 ford'],
            ["samsung galaxy tab a3ne s'allumeplus que faire"],
            ['最終痴漢電車 walkthrough'],
            ['木刀 teaduire en français'],
            ['テクノアーツ目黒区'],
            ['☀️ kss kss', 'zzzzt'],
            ['""th�me:strasa - mono"" wwwbf com'],
            ['casque blutouth r�ducteur de bruit'],
            ['famine  en afrique  subsha�rienne'],
            ["rapport«mission monnaies locales complémentaires»"],
            ['première partieavril 2015p', '29/76sylvio   gesel'],
            ['calucler temp après chauffe j/(kg°c)'],
            ['¢£¤§¨©«­®°²³´µ·¹º»¼½¿É×ßàáâãäåæçèéêëìíîïñòóôö÷øùúûüýþÿăćĉďđē'],
            ['¢£¤§¨©«­®°²³´µ·¹º»¼½¿ É ßàáâãäåæçèéêëìíîïñòóôö ÷ øùúûüýþÿăćĉďđē'],
            ['ėğĥīıĺľłńőœŕŝşšţźɔəʊʼˋ˜̧̀́̂̈έαγδεηθικλμνξοπρςστυωώвийкортцابةتجدرسع'],
            ['ėğĥīıĺľłńőœŕŝşšţźɔəʊ ʼˋ˜ έαγδεηθικλμνξοπρςστυωώвийкортцابةتجدرسع'],
            ['فقكلمهيẑếễỏ‐‑–—‘’‚‟†•…‬‹⁄ⁿ₁€™−√≠▒►☀', 'イウエガクコジプホムレンー三不与'],
            ['فقكلمهي ẑếễỏ ‐‑–—‘’‚‟†•…‬‹⁄ⁿ₁€™−√≠▒►☀', 'イウエガクコジプホムレンー三不与'],
            ['世了儿兼凡刀到可安平得掌晚木毛波海清熊猫界的认郭鱼默꼭바숨질ﬂ️﻿，�'],
            ['世了儿兼凡刀到可安平得掌晚木毛波海清熊猫界的认郭鱼默꼭바숨질 ﬂ ️﻿， �'],
        ]

        sentences = [
            str_utils.sentences(text)
            for text in self.examples]

        self.assertEqual(ref_examples, sentences)

    def test_characters(self):
        source1 = self.examples[0].split()
        sample1 = [str_utils.get_characters(s) for s in source1]
        reference1 = [
            ['1', '2'],
            ['3', '3', '4'],
            ['4', '2', '3', '5', '2', '3'],
            ['5', '4', '3', '5', '3', '4']
        ]

        source2 = self.examples[-1].split()
        sample2 = [str_utils.get_characters(s) for s in source2]
        reference2 = [[], ['ﬂ'], ['，'], ['�']]

        self.assertEqual(reference1, sample1)
        self.assertEqual(reference2, sample2)

    def test_word(self):
        source1 = self.examples[0].split()
        sample1 = [str_utils.check_valid_word(s) for s in source1]
        reference1 = [False, False, False, False]

        source2 = self.examples[-1].split()
        sample2 = [str_utils.check_valid_word(s) for s in source2]
        reference2 = [False, True, False, False]

        source3 = self.examples[2].split()
        sample3 = [str_utils.check_valid_word(s) for s in source3]
        reference3 = [True, True, True, True]

        self.assertEqual(reference1, sample1)
        self.assertEqual(reference2, sample2)
        self.assertEqual(reference3, sample3)

    def test_en_apostrophe(self):
        kwargs = {
            'alphabet': 'LATIN',
            'lowercase': True,
            'apostrophe': 'en',
            'ignore_digits': False,
            'ignore_punctuation': 'noise-a',
            'tostrip': True,
            'keepalnum': False,
        }

        source1 = "I don't wanna go"
        sample1 = str_utils.clean_text(source1, **kwargs)
        reference1 = "i do n't wanna go"

        source2 = "Can't she just do it?"
        sample2 = str_utils.clean_text(source2, **kwargs)
        reference2 = "ca n't she just do it"

        source3 = "She'd better leave fast!"
        sample3 = str_utils.clean_text(source3, **kwargs)
        reference3 = "she d better leave fast"

        self.assertEqual(reference1, sample1)
        self.assertEqual(reference2, sample2)
        self.assertEqual(reference3, sample3)

    def test_remove_apostrophes(self):
        source1 = "de littérature et d' eau fraiche a blanchard"
        sample1 = str_utils.remove_spaces_apostrophes(source1)
        reference1 = "de littérature et d'eau fraiche a blanchard"

        source2 = 'recette tarte pẑte brisée pur  eurre'
        sample2 = str_utils.remove_spaces_apostrophes(source2)
        reference2 = "recette tarte pẑte brisée pur  eurre"

        source3 = "roue tvingo 14'' occasion"
        sample3 = str_utils.remove_spaces_apostrophes(source3)
        reference3 = "roue tvingo 14''occasion"

        self.assertEqual(reference1, sample1)
        self.assertEqual(reference2, sample2)
        self.assertEqual(reference3, sample3)
