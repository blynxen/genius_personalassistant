import re
from langdetect import detect

class ContentModeration:
    def __init__(self):
        """
        Inicializa a classe de moderação de conteúdo com listas de palavras proibidas para 
        múltiplos idiomas.
        """
        # Palavras proibidas por idioma
        self.prohibited_words = {
            'pt': [  
                'merda', 'porra', 'caralho', 'foda-se', 'desgraça', 'cacete', 'puta', 'puta que pariu',
                'filho da puta', 'vai se foder', 'cu', 'arrombado', 'babaca', 'bosta', 'imbecil', 'idiota',
                'moleque', 'vagabunda', 'piranha', 'escória', 'cachorra', 'trouxa', 'otário', 'palhaço',

                # Insultos Racionais e Discurso de Ódio
                'macaco', 'preto fedido', 'judeu maldito', 'favelado', 'moleque de rua', 'viado', 'bicha', 
                'gorda', 'aleijado', 'retardado', 'mongoloide', 'zé povinho', 'sapatão', 'traveco',
                'veado', 'cigano', 'turco fedido', 'chinês safado', 'muçulmano terrorista', 'mongol',
                
                # Assédio e Bullying
                'morra', 'se mata', 'ninguém te quer', 'ninguém te ama', 'fracassado', 'verme', 'burro',
                'você não vale nada', 'escroto', 'patético', 'lixo', 'insignificante', 'escória', 'desprezível',

                # Ofensas Relacionadas à Acessibilidade e Inclusão
                'retardado', 'autista', 'todo mundo aí é autista', 'parece que só tem retardado nessa empresa', 
                'um monte de autista', 'essa empresa é uma creche', 'bando de incapaz', 'todo mundo aí é doente', 
                'deficiente mental', 'retardados incompetentes', 'inclusão de merda', 'lugar cheio de aleijados', 
                'essa empresa é pra autista', 'empresa de maluco', 'idiotas especiais',

                # Conteúdo Sexual Explícito
                'puta', 'boquete', 'chupada', 'transar', 'sexo', 'rola', 'buceta', 'pica', 'pornô', 
                'nudes', 'chupar', 'trepar', 'gozar', 'orgasmo', 'fetiche', 'pornografia', 'ninfeta',

                # Drogas e Substâncias Ilegais
                'maconha', 'cocaína', 'crack', 'êxtase', 'LSD', 'heroína', 'drogado', 'cheirar', 
                'traficante', 'droga', 'fumado', 'baseado', 'beck', 'erva', 'pó', 'balinha', 'santo daime',

                # Ameaças e Violência
                'vou te matar', 'você merece morrer', 'destruir sua vida', 'quebrar sua cara', 'terrorista', 
                'bomba', 'explosão', 'estupro', 'agredir', 'violência', 'assassino', 'tortura', 'linchamento', 
                'morte', 'pistola', 'arma', 'bala', 'faca', 'sangrar', 'tiro', 'guerra', 'ataque', 'atirar',

                # Fraudes e Golpes
                'esquema de pirâmide', 'phishing', 'scam', 'golpe financeiro', 'cartão clonado', 
                'dinheiro fácil', 'ganhar dinheiro rápido', 'roubar', 'fraudar', 'lavar dinheiro', 'suborno',
                'propina', 'corrupção', 'especulação', 'manipulação de mercado', 'insider trading', 'crime financeiro',

                # Termos Sensíveis (Consultoria Jurídica)
                'lavagem de dinheiro', 'evasão fiscal', 'sonegação de impostos', 'crime fiscal', 'corrupção ativa', 
                'corrupção passiva', 'fraude empresarial', 'crimes de colarinho branco', 'subterfúgio legal', 
                'abuso de poder', 'apropriação indevida', 'conflito de interesses', 'delação premiada', 'extorsão', 
                'chantagem', 'fraude trabalhista', 'falsificação de documentos', 'pirataria', 'hackear', 'ransomware',

                # Outras Ameaças e Insultos
                'miserável', 'inútil', 'incompetente', 'burro', 'vagabundo', 'imbecil', 'tonto', 'covarde', 
                'canalha', 'covarde', 'cretino', 'maldito', 'ridículo', 'besta', 'bruxa', 'peste', 'venenoso',

                # Termos Desrespeitosos Relacionados à Empresa e Funcionários
                'empresa de merda', 'esse sistema é um lixo', 'sua equipe é inútil', 'só tem incompetente aí', 
                'atendimento péssimo', 'vou processar', 'vou levar à justiça', 'seus produtos são um lixo', 
                'vou te botar no tribunal', 'esse serviço é uma vergonha', 'falta de profissionalismo', 
                'vou abrir uma reclamação', 'vocês vão falir', 'incompetência generalizada', 'trabalho mal feito', 
                'todos aí são um bando de retardados', 'empresa de autistas', 'seus merdas', 'bando de otários',
                'bando de burros', 'seus inúteis', 'não servem pra nada', 'lixo de empresa', 'lugar de loucos', 
                'ninguém aí presta', 'empresa inclusiva de merda', 'esse negócio de inclusão não funciona', 
                'empresa de retardados', 'autistas incapazes'
            ],
            'en': [  
                # Swear Words and Offensive Language
                'shit', 'fuck', 'damn', 'bastard', 'bitch', 'asshole', 'fucker', 'motherfucker', 'crap', 'dick', 
                'cunt', 'whore', 'piss off', 'scumbag', 'douchebag', 'jerk', 'idiot', 'loser', 'moron', 'freak',

                # Racial Insults and Hate Speech
                'nigger', 'chink', 'spic', 'kike', 'wetback', 'faggot', 'tranny', 'dyke', 'fat ass', 'cripple', 
                'retard', 'gook', 'sand nigger', 'camel jockey', 'terrorist', 'illegal alien', 'white trash',

                # Bullying and Harassment
                'kill yourself', 'nobody loves you', 'worthless', 'pathetic', 'loser', 'garbage', 'useless', 
                'disgusting', 'you are nothing', 'cretin', 'go die', 'failure', 'scum',

                # Offensive Terms Related to Accessibility and Inclusion
                'retard', 'autistic', 'everyone working here is retarded', 'bunch of autistic people', 'this company is a daycare', 
                'disabled idiots', 'this place is full of retards', 'you all are mentally challenged', 'cripple', 
                'company full of handicaps', 'inclusion sucks', 'autistic losers', 'mental cases', 'crazy house', 'useless cripples',

                # Sexual Content and Innuendos
                'porn', 'boobs', 'tits', 'dick', 'cock', 'pussy', 'vagina', 'ass', 'suck my dick', 'blowjob', 
                'nudes', 'orgasm', 'fetish', 'bang', 'fuck buddy', 'rape', 'molester', 'pedophile', 'slut',

                # Drugs and Illegal Substances
                'weed', 'cocaine', 'heroin', 'meth', 'crack', 'LSD', 'ecstasy', 'drug dealer', 'stoner', 'high', 
                'junkie', 'blunt', 'pot', 'dope', 'tripping', 'snorting', 'shooting up',

                # Threats and Violence
                'I will kill you', 'you deserve to die', 'I will beat you up', 'bomb', 'terrorist', 'gun', 
                'shoot', 'murder', 'stab', 'explode', 'assault', 'rape', 'kill', 'war', 'massacre', 'slaughter',

                # Fraud and Scams
                'pyramid scheme', 'phishing', 'scam', 'identity theft', 'credit card fraud', 'easy money', 
                'get rich quick', 'money laundering', 'embezzlement', 'bribery', 'extortion', 'insider trading', 
                'tax evasion', 'market manipulation', 'corporate fraud', 'kickbacks',

                # Sensitive Legal Terms (Consulting Context)
                'money laundering', 'tax evasion', 'white collar crime', 'bribery', 'corporate espionage', 
                'embezzlement', 'insider trading', 'fraudulent activity', 'fraudulent business', 'power abuse', 
                'conflict of interest', 'fraudulent contracts', 'illegal contracts', 'fraudulent practices',

                # Other Threats and Insults
                'loser', 'moron', 'idiot', 'incompetent', 'stupid', 'bastard', 'jerk', 'coward', 'scum', 'trash', 
                'disgusting', 'worthless', 'failure', 'cretin', 'lazy',

                # Disrespectful Business-related Terms
                'your company is garbage', 'this system sucks', 'your team is useless', 'horrible service', 
                'this product is crap', 'I’ll sue you', 'this service is a joke', 'lack of professionalism', 
                'I’m reporting you', 'you will go bankrupt', 'you guys are incompetent', 'poorly done work', 
                'all of you are retarded', 'your company is full of autistic people', 'you are all idiots', 
                'your staff is useless', 'a bunch of lazy retards', 'this company is full of freaks', 
                'inclusion doesn’t work', 'useless autistic employees', 'idiots running a circus'
            ],
            'es': [  
                ## Palabras de bajo calão y lenguaje ofensivo
                "mierda", "joder", "maldito", "bastardo", "zorra", "imbécil", "cabron", 
                "hijo de puta", "polla", "coño", "puta", "gilipollas", "vete a la mierda", 
                "asqueroso", "idiota", "perdedor", "miserable", "freak",
                
                ## Insultos raciales y discurso de odio
                "negro", "chino", "sudaca", "judío", "espalda mojada", "maricón", 
                "tranny", "torta", "gordo", "lisiado", "retrasado", "amarillo", 
                "moro", "jodido terrorista", "extranjero ilegal", "blanco basura",
                
                ## Bullying y acoso
                "suicídate", "nadie te quiere", "inútil", "patético", "perdedor", 
                "basura", "asqueroso", "no eres nada", "cretino", "muérete", "fracaso", "escoria",
                
                ## Términos ofensivos relacionados con accesibilidad e inclusión
                "retrasado", "autista", "todos los que trabajan aquí son retrasados", 
                "un montón de autistas", "esta empresa es una guardería", "idiotas discapacitados", 
                "esta empresa está llena de retrasados", "todos ustedes son mentalmente incapacitados", 
                "lisiado", "empresa llena de discapacitados", "la inclusión apesta", 
                "perdedores autistas", "casos mentales", "manicomio", "lisiados inútiles",
                
                ## Contenido sexual e insinuaciones
                "porno", "tetas", "polla", "verga", "coño", "vagina", "culo", 
                "chúpame la polla", "mamada", "desnudos", "orgasmo", "fetiche", 
                "follar", "amigo con derecho", "violación", "abusador", "pedófilo", "puta",
                
                ## Drogas y sustancias ilegales
                "marihuana", "cocaína", "heroína", "meta", "crack", "LSD", "éxtasis", 
                "narcotraficante", "drogado", "colocado", "adicto", "porro", "droga", 
                "viajando", "esnifando", "inyectando",
                
                ## Amenazas y violencia
                "te voy a matar", "mereces morir", "te voy a dar una paliza", "bomba", 
                "terrorista", "pistola", "disparo", "asesinato", "apuñalar", "explotar", 
                "agresión", "violación", "matar", "guerra", "masacre", "carnicería",
                
                ## Fraude y estafas
                "esquema piramidal", "phishing", "estafa", "robo de identidad", 
                "fraude con tarjetas de crédito", "dinero fácil", "hazte rico rápido", 
                "lavado de dinero", "malversación", "soborno", "extorsión", 
                "uso de información privilegiada", "evasión de impuestos", "manipulación del mercado", 
                "fraude corporativo", "comisiones ilegales",
                
                ## Términos legales sensibles (Consultoría)
                "lavado de dinero", "evasión de impuestos", "delito de cuello blanco", 
                "soborno", "espionaje corporativo", "malversación", "uso de información privilegiada", 
                "actividad fraudulenta", "empresa fraudulenta", "abuso de poder", 
                "conflicto de intereses", "contratos fraudulentos", "prácticas ilegales",
                
                ## Otras amenazas e insultos
                "perdedor", "imbécil", "idiota", "incompetente", "estúpido", "bastardo", 
                "gilipollas", "cobarde", "escoria", "basura", "asqueroso", "inútil", 
                "fracaso", "cretino", "vago",
                
                ## Términos irrespetuosos relacionados con los negocios
                "tu empresa es basura", "este sistema apesta", "tu equipo es inútil", 
                "servicio horrible", "este producto es una mierda", "te voy a demandar", 
                "este servicio es una broma", "falta de profesionalismo", "te voy a denunciar", 
                "quebrarás", "ustedes son incompetentes", "trabajo mal hecho", 
                "todos ustedes son retrasados", "su empresa está llena de autistas", 
                "todos son idiotas", "tu personal es inútil", "un montón de retrasados perezosos", 
                "esta empresa está llena de monstruos", "la inclusión no funciona", 
                "empleados autistas inútiles", "idiotas manejando un circo"
            ]
        }

    def detect_language(self, text):
        """
        Detecta o idioma do texto utilizando a biblioteca `langdetect`.
        :param text: Texto para detecção de idioma.
        :return: O código de idioma detectado (e.g., 'pt', 'en', 'es').
        """
        try:
            return detect(text)
        except:
            return 'pt'  # Se não conseguir detectar, assume português por padrão

    def contains_inappropriate_content(self, text):
        """
        Verifica se o texto contém palavras proibidas, com base no idioma detectado.
        :param text: Texto para verificação de conteúdo inapropriado.
        :return: True se houver palavras proibidas, False caso contrário.
        """
        language = self.detect_language(text)
        prohibited_words = self.prohibited_words.get(language, [])
        for word in prohibited_words:
            if re.search(r'\b' + re.escape(word) + r'\b', text.lower()):
                return True
        return False

    def moderate_content(self, text):
        """
        Modera o conteúdo removendo ou substituindo palavras proibidas com base no idioma.
        :param text: Texto para moderação.
        :return: Texto moderado, com palavras proibidas substituídas.
        """
        language = self.detect_language(text)
        prohibited_words = self.prohibited_words.get(language, [])
        for word in prohibited_words:
            # Substitui as palavras proibidas por "[conteúdo removido]"
            text = re.sub(r'\b' + re.escape(word) + r'\b', "[conteúdo removido]", text, flags=re.IGNORECASE)
        return text
