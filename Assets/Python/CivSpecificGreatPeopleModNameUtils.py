#  Civ-Specific Great People 2.0
#  Created by Gaius Octavius
#  Python version for Beyond the Sword, December 2007
#
#  Adapted from the No-Name Renamer Mod by TheLopez
#  All names collected and categorized by Gaius Octavius

from CvPythonExtensions import *

import CvUtil
import sys
import math
import string

gc = CyGlobalContext()

# Random/Sequential Naming Option - Switch to 0 or 1 depending on your preference. Default is True (randomized names).
RandomNameOrder = 1


# The main civ-specific list
civilizationNameHash =	{ 
							"CIVILIZATION_AMERICA" :
							{
								"GP" : ("William Penn", "Roger Williams", "Jonathan Edwards", "Joseph Smith", "Sojourner Truth"),
								"GA" : ("Edgar Allan Poe", "Herman Melville", "Mark Twain", "Ernest Hemingway", "Charlie Chaplin", "Elvis Presley", "Miles Davis", "Jimi Hendrix"),
								"GS" : ("Arthur Compton", "Edwin Hubble", "John von Neumann", "Glenn Seaborg", "Robert Oppenheimer", "Richard Feynman"),
								"GE" : ("Benjamin Franklin", "Thomas Edison", "Nichola Tesla", "Henry Ford", "Orville Wright", "Charles Goodyear"),
								"GM" : ("Cornelius Vanderbilt", "John D. Rockefeller", "Andrew Carnegie", "William Edward Boeing", "Bill Gates"),
								"GG" : ("Andrew Jackson", "Ulysses C. Grant", "Robert E. Lee", "Dwight D. Eisenhower", "George Patton", "Douglas MacArthur"),
								"GSPY" : ("Great American Spy")
							},
							"CIVILIZATION_ROME" :
							{
								"GP" : ("Tarpeia", "Aquilia Severa", "Augustinus", "Thomas Aquinas", "Eusebius"),
								"GA" : ("Livius", "Vergil", "Ovid", "Plutarch", "Seneca", "Juvenal"),
								"GS" : ("Strabo", "Cato", "Cicero", "Plinius", "Sosigenes"),
								"GE" : ("Agrippa", "Apollodorus", "Hitarius", "Vitruvius"),
								"GM" : ("Jucundus", "Sittius", "Atticus", "Marcus L. Crassus"),
								"GG" : ("Scipio Africanus", "Gaius Marius", "Pompeius", "Vespasian", "Trajan", "Hadrian"),
								"GSPY" : ("Great Roman Spy")
							},
							"CIVILIZATION_EGYPT" :
							{
								"GP" : ("Moses", "Akhenaten", "Ptahhotep", "Mehryra", "Petiese"),
								"GA" : ("Khaemweset", "Yuny", "Ineni", "Amenemhat", "Khafre", "Amenhotep", "Nefertari"),
								"GS" : ("Merit Ptah", "Ptolemaios", "Hypatia", "Conon", "Diophantos", "Manetho"),
								"GE" : ("Imhotep", "Khaemwase", "Zoser", "Snefru", "Senemut", "Kha"),
								"GM" : ("Harkuf", "Piye", "Alara", "Maya", "Ahmose"),
								"GG" : ("Menes", "Khufu", "Mentuhotep", "Seti", "Narmer", "Thotmosis"),
								"GSPY" : ("Great Egyptian Spy")
							},
							"CIVILIZATION_GREECE" :
							{
								"GP" : ("Herakleitos", "Parmenides", "Epikuros", "Philolaos", "Anacharsis"),
								"GA" : ("Homeros", "Thukydides", "Sophokles", "Euripides", "Herodotos", "Aeschylos"),
								"GS" : ("Sokrates", "Platon", "Aristoteles", "Eukleides", "Pythagoras", "Erastothenes", "Demokritos", "Anaxagoras", "Galenos", "Hippokrates"),
								"GE" : ("Archimedes", "Heron", "Thales", "Zenon", "Empedokles", "Satyros"),
								"GM" : ("Pytheas", "Kroisos", "Androsthenes", "Megasthenes"),
								"GG" : ("Leonidas", "Lysandros", "Pyrrhos", "Hektor", "Philippos", "Themistokles"),
								"GSPY" : ("Great Greek Spy")
							},
							"CIVILIZATION_GERMANY" :
							{
								"GP" : ("Hildegard von Bingen", "Albertus Magnus", "Martin Luther", "Philip Melanchthon", "Jan Hus", "Albert Schweitzer", "Dietrich Bonhoeffer"),
								"GA" : ("Albrecht D&#252;rer", "Johann Sebastian Bach", "Ludwig van Beethoven", "Wolfgang Amadeus Mozart", "Johann Wolfgang von Goethe", "Friedrich Schiller", "Franz Kafka"),
								"GS" : ("Nikolaus Kopernikus", "Johannes Kepler", "Carl Friedrich Gauss", "Gottfried Leibniz", "Albert Einstein", "Werner Heisenberg", "Erwin Schr&#246;dinger", "Max Planck"),
								"GE" : ("Wilhelm Schickard", "Johannes Gutenberg", "Nikolaus August Otto", "Gottlieb Daimler", "Fritz Haber", "Wernher von Braun", "Otto Hahn"),
								"GM" : ("Gerhard Mercator", "Jakob Fugger", "August Horch", "Ferdinand Porsche", "Carl Benz"),
								"GG" : ("Arminius", "Friedrich Barbarossa", "Albrecht von Wallenstein", "Gebhard Leberecht von Bl&#252;cher", "Carl von Clausewitz", "Paul von Hindenburg", "Erwin Rommel", "Heinz Guderian"),
								"GSPY" : ("Great German Spy")
							},
							"CIVILIZATION_RUSSIA" :
							{
								"GP" : ("Paisiy Yaroslavov", "Feofan Prokopovich", "Nikolai Berdyaev", "Georges Florovsky", "Alexei Losev"),
								"GA" : ("Leo Tolstoi", "Anton Chekov", "Fyodor Dostoyevsky", "Pyotr Ilyich Tchaikovsky", "Modest Mussorgsky"),
								"GS" : ("Mikhail Lomonosov", "Nikolai Lobachevsky", "Dmitri Mendeleyev", "Mikhail Ostrogradsky", "Pavel Cherenkov"),
								"GE" : ("Ivan Starov", "Sergei Korolev", "Leon Theremin", "Vladimir Zworykin", "Andrey Tupolev", "Igor Sikorsky"),
								"GM" : ("Ivan Kruzenshtern", "Vitus Bering", "Afanasiy Nikitin"),
								"GG" : ("Alexander Nevsky", "Mikhail Romanov", "Alexander Suvorov", "Pavel Nakhimov", "Mikhail Skobelev", "Georgy Zhukov", "Vasily Chuikov"),
								"GSPY" : ("Great Russian Spy")
							},
							"CIVILIZATION_CHINA" :
							{
								"GP" : ("Meng Zi", "Han Fei", "Kong Fuzi", "Zhuang Zi", "Lao Tzu"),
								"GA" : ("Li Bo", "Du Fu", "Wang Xizhi", "Ling Lun", "Su Shi"),
								"GS" : ("Zu Chongzhi", "Liu Hui", "Li Fan", "Zhu Shijie", "Yuan Lee", "Chen Ning Yang"),
								"GE" : ("Cai Lun", "Qian Saqiang", "Zhang Heng", "Bi Sheng", "Li Siguang", "Xiaoyun Wang"),
								"GM" : ("Zhang Qian", "Wang Anshi", "Zheng He", "Lo Hong-Shui", "Zhou Zhengyi"),
								"GG" : ("Sun Tzu", "Cao Cao", "Zhuge Liang", "Guo Ziyi", "Shi Lang", "Zhang Zuolin", "Chiang Kai-shek"),
								"GSPY" : ("Great Chinese Spy")
							},
							"CIVILIZATION_ENGLAND" :
							{
								"GP" : ("Venerable Bede", "Anselm of Canterbury", "Thomas Becket", "Thomas More", "John Newton", "William Booth"),
								"GA" : ("William Shakespeare", "John Milton", "Charles Dickens", "Arthur Conan Doyle", "JRR Tolkien", "John Lennon", "Elton John"),
								"GS" : ("Isaac Newton", "Francis Bacon", "John Dalton", "James Clerk Maxwell", "Charles Darwin", "Ernest Rutherford", "Stephen Hawking"), 
								"GE" : ("Henry Bessemer", "James Watt", "Charles Babbage", "Alan Turing", "James Dyson"),
								"GM" : ("Francis Drake", "James Cook", "Adam Smith", "John Maynard Keynes"),
								"GG" : ("William the Conqueror", "Edward Longshanks", "Richard the Lionhearted", "Oliver Cromwell", "Horatio Nelson", "Arthur Wellesley of Wellington", "Louis Mountbatten", "Bernard Law Montgomery"),
								"GSPY" : ("Great English Spy")
							},
							"CIVILIZATION_JAPAN" :
							{
								"GP" : ("Kobo-Daishi", "Nikko Shonin", "Takuan Soho", "Shinran", "Eisai Zenji", "Uchimura Kanzo"),
								"GA" : ("Saigyo Hoshi", "Kano Eitoku", "Toshusai Sharaku", "Katsushika Hokusai", "Utagawa Hiroshige"),
								"GS" : ("Aida Yasuaki", "Kiyoshi Ito", "Hideki Yukawa", "Kenkichi Iwasawa", "Masatoshi Koshiba"),
								"GE" : ("Kyota Sugimoto", "Hidetsugu Yagi", "Kotaro Honda", "Ken Sakamura", "Shigeru Miyamoto"),
								"GM" : ("Masahisa Fujita", "Torakusu Yamaha", "Kiichiro Toyoda", "Yoshitaka Fukuda", "Soichiro Honda"),
								"GG" : ("Fujiwara no Kamatari", "Ashikaga Takauji", "Minamoto no Yoritomo", "Toyotomi Hideyoshi", "Togo Heihachiro", "Tomoyuki Yamashita", "Isoroku Yamamoto"),
								"GSPY" : ("Great Japanese Spy")
							},
							"CIVILIZATION_FRANCE" :
							{
								"GP" : ("Pierre Abelard", "Louis Capet", "Jean Calvin", "Hubert Languet", "Marcel L&#233;gaut"),
								"GA" : ("Victor Hugo", "Claude Monet", "Fran&#231;ois Truffaut", "Henri Matisse", "Claude Debussy", "Alexandre Dumas"),
								"GS" : ("Louis Pasteur", "Rene Descartes", "Antoine Lavoisier", "Pierre-Simon Laplace", "Pierre de Fermat", "Antoine Henri Becquerel", "Marie Curie"),
								"GE" : ("Blaise Pascal", "Charles Augustin de Coulomb", "Alexandre Gustave Eiffel", "Claude Perrault", "Joseph-Michel Montgolfier"),
								"GM" : ("Jacques Cartier", "Coco Chanel", "Samuel de Champlain", "Marcel Dassault", "Liliane Bettencourt"),
								"GG" : ("Charles Martel", "Louis-Joseph de Montcalm", "Gilbert de Lafayette", "Louis-Rene de Latouche Treville", "Louis-Nicolas Davout"),
								"GSPY" : ("Great French Spy")
							},
							"CIVILIZATION_INDIA" :
							{
								"GP" : ("Mahavira", "Shankara", "Siddharta Gautama", "Tipu Sultan", "Ananda", "Atisha"),
								"GA" : ("Valmiki", "Kalidas", "Raja Rao", "Rabindranath Tagore", "Basawan"),
								"GS" : ("Aryabhata", "Brahmagupta", "Bhaskara", "Nilakantha Somayaji", "Madhava", "Kamalakara"),
								"GE" : ("Baudhayana", "Chandrasekhara Venkata Raman", "Jagadish Bose", "Lagadha"),
								"GM" : ("Raja Todar Mal", "Shah Jahan", "Jamshetji Tata", "Ardeshir Godrej"),
								"GG" : ("Chandragupta Maurya", "Samudragupta Maurya", "Rajaraja Chola", "Shivaji Bhosle"),
								"GSPY" : ("Great Indian Spy")
							},
 							"CIVILIZATION_PERSIA" :
							{
								"GP" : ("Zoroaster", "Mani", "Mazdak", "Zahed Gilani", "Jalal al-Din al-Rumi", "Mulla Sadra"),
								"GA" : ("Safi Al-Din", "Abu-Muhammad Shirazi", "Firdausi", "Reza Abbasi", "Kamal ud-Din Behzad"),
								"GS" : ("Ardashir", "Al-Khwarizmi", "Al-Razi", "Ibn Sina", "Azophi", "Zakariya Masawaiyh"),
								"GE" : ("Artaxerxes", "Bahram", "Al-Khujandi", "Ibn al-Haitham"),
								"GM" : ("Kavadh", "Ahmad ibn Rustah", "Istakhri", "Ahmad-e Roste Esfahani"),
								"GG" : ("Achaemenes", "Xerxes", "Shapur", "Abbas", "Mithridates"),
								"GSPY" : ("Great Persian Spy")
							},
							"CIVILIZATION_AZTEC" :
							{
								"GP" : ("Tlacateotl", "Tenoch", "Papantzin", "Yacotzin", "Ixtlilxochitl"),
								"GA" : ("Cipactli", "Oxomoco", "Huitzilopochtli", "Techotlalatzin", "Ihuitemotzin"),
								"GS" : ("Chichatoyotl", "Textalatzin", "Axayacatl", "Ixtlilxochitl", "Coanacochtzin"),
								"GE" : ("Xolotl", "Itzcatl", "Mixcoatl", "Tlacaelel", "Moquihuix"),
								"GM" : ("Cuauhtemoc", "Tlacotzin", "Chak-Mol", "Atlante", "Techichpotzin"),
								"GG" : ("Ahuitzotl", "Itzcoatl", "Huitzilhuitl", "Chimalpopoca", "Maxtla", "Tezozomoc"),
								"GSPY" : ("Great Aztec Spy")
							},
							"CIVILIZATION_MONGOL" :
							{
								"GP" : ("Chabi", "Zanabazar", "Abaqa", "Arghun", "Sartaq"),
								"GA" : ("Siqin Gaowa", "Oghul Ghaymish", "Tolui", "Uzbeg Khan"),
								"GS" : ("Minzu Wenyibao", "Nurhaci", "Dayan Khan", "Kaidu", "Mandukhai Khatun"),
								"GE" : ("Li Siguang", "Ulan Bator", "Zhang Wenqian", "Toqta", "Duwa"),
								"GM" : ("Altan Khan", "Hulagu", "Gaykhatu", "G&#252;y&#252;k", "Mengu-Timur"),
								"GG" : ("Ogadei", "Chagatai", "Toghril", "M&#246;ngke", "Timur Lenk"),
								"GSPY" : ("Great Mongolian Spy")
							},
							"CIVILIZATION_SPAIN" :
							{
								"GP" : ("Ignatius Loyola", "Junipero Serra", "Bartolome de Las Casas", "Juan de Sepulveda", "Francisco Suarez"),
								"GA" : ("Miguel de Cervantes", "Diego de Silva Velazquez", "Garcilaso de la Vega", "Pablo Picasso", "Salvador Dal&#237;"),
								"GS" : ("Juan de Ortega", "Gherard de Cremona", "Joao Baptista Lavanha", "Santiago Ram&#243;n y Cajal", "Antonio de Ulloa"),
								"GE" : ("Juan de Herrera", "Juan de la Cierva", "Esteban Terradas i Illa", "Alberto Palacio", "Agust&#237;n de Betancourt"),
								"GM" : ("Cristoforo Colombo", "Ferdinand Magellan", "Hernando de Soto", "Vasco da Gama", "Salvador Fidaldo"),
								"GG" : ("El Cid Campeador", "Francisco Coronado", "Hernando Cortes", "Francisco Pizarro", "Ambrosio Spinola Doria", "Alvaro de Bazan"),
								"GSPY" : ("Great Spanish Spy")
							},
							"CIVILIZATION_VIKING" :
							{
								"GP" : ("Harold Bluetooth", "Sweyn Forkbeard", "Aethelstan", "Gisbertus Voetius", "Jacobus Arminius"),
								"GA" : ("Johan Nordahl Brun", "Olav Duun", "Hans Christian Andersen", "Johan Ludvig Runeberg"),
								"GS" : ("Anders Angstrom", "Tycho Brahe", "Johannes Rydberg", "Ole R&#248;mer", "Anders Celsius", "Niels Bohr"),
								"GE" : ("Ivar Giaver", "Sophus Lie", "Niels Abel", "Alfred Nobel", "Linus Torvalds"),
								"GM" : ("Leif Eriksson", "Haakon Sigurdsson", "Ingvar Kamprad", "Roald Amundsen"),
								"GG" : ("Eric Bloodaxe", "Harald Hardraada", "Canute II", "Gustav Vasa"),
								"GSPY" : ("Great Scandinavian Spy")
							},
							"CIVILIZATION_OTTOMAN" :
							{
								"GP" : ("Rumi", "Sokollu Mehmet Pasha", "Mustafa Cagrici", "Yaakov Culi", "Sabbatai Zevi"),
								"GA" : ("Yunus Emre", "Hayali", "Gul Baba", "Mehmet Akif Ersoy", "Atik Sinan"),
								"GS" : ("Thabit Ibn Qurra", "Cahit Arf", "Qazi Zadeh", "Oktay Sinanoglu", "Feza G&#252;rsey"),
								"GM" : ("Evliya Celebi", "Abdulmecid", "Hormuzd Rassam", "Nejat Eczacibasi", "Aydin Dogan"),
								"GE" : ("Sinan", "Nitam-al-Mulk", "Al-Ghazali", "Ratip Berker", "Ekmel Ozbay"),
								"GG" : ("Orhan", "Selim", "Bayezid", "Turgut Reis", "Ismail Enver", "Ibrahim Pasha"),
								"GSPY" : ("Great Turkish Spy")
							},
							"CIVILIZATION_ARABIA" :
							{
								"GP" : ("Ali ibn Abi Talib", "Al-Farabi", "Hasan", "Ismail", "Al-Baqilani", "Abd-al-Wahhab", "Umar ibn al-Khattab", "Uthman"),
								"GA" : ("Ibn Muqlah", "Al-Mutanabbi", "Ibn Quzman", "Ibn al-Nadim", "Ibn Furtu", "Yaqut al-Hamawi"),
								"GS" : ("Alhazen", "Al-Kindi", "Uthman al-Sabuni", "Ibrahim ibn Sinan", "Al-Zarqali", "Ibn Al-Jazzar", "Al-Qabizi"),
								"GE" : ("Ali Abbas", "Al-Jazari", "Jabir ibn Hayyan", "Abbas ibn Firnas", "Ibn Wahshiyah"),
								"GM" : ("Ibn Battuta", "Ahmad ibn Majid", "Ibn Jubayr", "Ibn Hawqal", "Al-Idrisi"),
								"GG" : ("Mu'awiya", "Ziyad Ibn Abihi", "Ahmah al-Mansur", "Yusuf ibn Tashfin", "Khalid ibn Al-Walid", "Amr ibn al-As"),
								"GSPY" : ("Great Arabian Spy")
							},
							"CIVILIZATION_CARTHAGE" :
							{
								"GP" : ("Acherbas", "Tertullian", "Cyprian", "Donatus"),
								"GA" : ("Kartobal", "Orthobal", "Sophonisba", "Oxyntas", "Micipsa"),
								"GS" : ("Bomilcar", "Tanit", "Eshmuniaton", "Mago", "Hiram"),
								"GE" : ("Gauda", "Zelalsen", "Gala", "Malchus"),
								"GM" : ("Hanno", "Adherbal", "Himilco", "Bocchus"),
								"GG" : ("Hamilcar Barca", "Hasdrubal Barca", "Maharbal", "Mago Barca", "Cathalo", "Himilco"),
								"GSPY" : ("Great Phoenicican Spy")
							},
							"CIVILIZATION_INCA" :
							{
								"GP" : ("Guyasuta", "Yahuar Huacac"),
								"GA" : ("Ah Cacao", "Viracocha", "Ninan Cuyochi", "Ocllo"),
								"GS" : ("Sinchi Roca", "Manco Capac", "Maita Capac", "Titu Cusi", "Huascar", "Inca Roca"),
								"GE" : ("Sipan-Itchi", "Mana-Paoa", "Kenu Curaua", "Sayri Tupa Inca", "Capac Yupanqui"),
								"GM" : ("Tupa Inca-Yupanqui", "Felipillo", "Quetzal-Macau"),
								"GG" : ("Pachacuti", "Manco Inca", "Tupa Amaru", "Atahualpa", "Chalicuchima", "Quisquis"),
								"GSPY" : ("Great Incan Spy")
							},
							"CIVILIZATION_MALI" :
							{
								"GP" : ("Ali Coulibaly", "Wali Keita", "Seku Amadu", "Sidi Yahya"),
								"GA" : ("Nare Maghann Konate", "Gao", "Lobi Traore", "Abd Arahman ibn Faqi Mahmud", "Ibrahima Aya"),
								"GS" : ("Mahmud", "Ahmed Baba", "Ag Mohammed", "Abu al Baraaka", "Gaoussou Diawara"),
								"GE" : ("Al-Qadi Aqib ibn Umar", "Abu Es Haq es Saheli", "Mohammed Bagayogo", "Sakura", "Mohamed Naddah"),
								"GM" : ("Abubakari", "Abu Bakr ibn Ahmad Biru", "Wali Keita", "Moctar Ouane", "Tunka Manin"),
								"GG" : ("Askia Muhammad", "Askia Daud", "Sunni Ali", "Sundiata", "Ngolo Diarra"),
								"GSPY" : ("Great Malian Spy")
							},
							"CIVILIZATION_BYZANTIUM" :
							{
								"GP" : ("Photios", "Michael Kerularios", "Ioannis Xiphilinos", "Nikolaos Mystikos", "Damaskios", "Gregorios o Nazianzos"),
								"GA" : ("Theophylaktos Simokates", "Theophanes Strelitzas", "Georgios Plethon", "Manuel Chrysoloras", "Ioannis Kukuzelis"),
								"GS" : ("Stephanos Alexandrinos", "Georgios Hermonymos", "Anna Comnena", "Demetrios Triklinios", "Nikephoros Blemmydes", "Nicholas Myrepsos"),
								"GE" : ("Anthemios o Tralleis", "Isidor o Milet", "Eutokios o Askalon", "Kallinikos o Heliopolis", "Leontios"),
								"GM" : ("Hierokles", "Loukas Notaras", "Theophoros", "Zemarchos"),
								"GG" : ("Belisarios", "Herakleios", "Maurikios", "Basileios Bulgaroktonos", "Alexios Komnenos", "Michael Palaiologos"),
								"GSPY" : ("Great Byzantine Spy")
							},
							"CIVILIZATION_PORTUGAL" :
							{
								"GP" : ("Fernando de Bulh&#245;es", "Isabel de Aragao", "Joao de Deus"),
								"GA" : ("Fern&#227;o Lopes", "Ruy de Pina", "Garcia de Resende", "Lu&#237;s de Cam&#245;es", "Ant&#243;nio Ferreira"),
								"GS" : ("Pedro Nunes", "Garcia de Orta"),
								"GE" : ("Diogo Boitac", "Mateus Fernandes", "Diogo de Arruda"),
								"GM" : ("Vasco da Gama", "Pedro &#193;lvares Cabral", "Henrique o Navegador"),
								"GG" : ("Nuno &#193;lvares Pereira"),
								"GSPY" : ("Great Portuguese Spy")
							},
							"CIVILIZATION_NETHERLANDS" :
							{
								"GP" : ("Abraham Kuyper", "Erasmus van Rotterdam"),
								"GA" : ("Rembrandt van Rijn", "Vincent van Gogh", "Johannes Vermeer", "Hendrick de Keyser", "Pieter Corneliszoon Hooft"),
								"GS" : ("Christiaan Huygens", "Simon Stevin", "Govert Bidloo"),
								"GE" : ("Jan Leeghwater", "Cornelis Corneliszoon", "Anton van Leeuwenhoek"),
								"GM" : ("Pieter Stuyvesant", "Abel Tasman", "Willem Barentz", "Cornelis de Houtman", "Jan van Riebeeck", "Jan Coen", "Antony van Diemen"),
								"GG" : ("Maurits van Nassau", "Frederik Hendrik", "Cornelis Tromp", "Michiel de Ruyter"),
								"GSPY" : ("Great Dutch Spy")
							},
							"CIVILIZATION_BABYLONIA" :
							{
								"GP" : ("Utnapishtim", "Ibrahim", "Younis"),
								"GA" : ("Gudea", "Samsu-ditana"),
								"GS" : ("Sin-leqi-unninni", "Tapputi-Belatekallim", "Sudines", "Kidenas"),
								"GE" : ("Ur-Nammu", "Nabupolassar", "Naram-sin", "Gudea"),
								"GM" : ("Burna-Briash", "Kadashman-Enlil"),
								"GG" : ("Sennacherib", "Tiglath-pileser", "Nebukadnezar", "Shalmaneser"),
								"GSPY" : ("Great Babylonian Spy")
							},
							"CIVILIZATION_KHMER" :
							{
								"GP" : ("Great Khmer Prophet"),
								"GA" : ("Great Khmer Artist"),
								"GS" : ("Great Khmer Scientist"),
								"GE" : ("Great Khmer Engineer"),
								"GM" : ("Great Khmer Merchant"),
								"GG" : ("Great Khmer General"),
								"GSPY" : ("Great Khmer Spy")
							},
							"CIVILIZATION_MAYA" :
							{
								"GP" : ("Great Mayan Prophet"),
								"GA" : ("Great Mayan Artist"),
								"GS" : ("Great Mayan Scientist"),
								"GE" : ("Great Mayan Engineer"),
								"GM" : ("Great Mayan Merchant"),
								"GG" : ("Great Mayan General"),
								"GSPY" : ("Great Mayan Spy")
							},
							"CIVILIZATION_ETHIOPIA" :
							{
								"GP" : ("Great Ethiopian Prophet"),
								"GA" : ("Great Ethiopian Artist"),
								"GS" : ("Great Ethiopian Scientist"),
								"GE" : ("Great Ethiopian Engineer"),
								"GM" : ("Great Ethiopian Merchant"),
								"GG" : ("Great Ethiopian General"),
								"GSPY" : ("Great Ethiopian Spy")
							},
							"CIVILIZATION_ITALY" :
							{
								"GP" : ("Francesco d'Assisi", "Alfonso de Borgia", "Giulio de' Medici", "Camillo Borghese"),
								"GA" : ("Michelangelo", "Dante Alighieri", "Sandro Botticelli", "Nicolo Macchiavelli", "Donatello", "Raphael", "Gabriele Trovato"),
								"GS" : ("Francesco Petrarca", "Pico della Mirandola", "Galileo Galilei", "Luigi Galvani", "Guglielmo Marconi", "Enrico Fermi"),
								"GE" : ("Leonardo da Vinci", "Taccola", "Filippo Brunelleschi", "Donato Bramante", "Alessandro Volta"),
								"GM" : ("Simone de' Bardi", "Donato Peruzzi", "Giovanni de'Medici", "Ciriaco de Ancona"),
								"GG" : ("Lorenzo de' Medici", "Enrico Dandolo", "Francesco Sforza", "Giuseppe Garibaldi"),
								"GSPY" : ("Great Italian Spy")
							},
							"CIVILIZATION_NATIVE" :
							{
								"GP" : ("Great Native Prophet"),
								"GA" : ("Great Native Artist"),
								"GS" : ("Great Native Scientist"),
								"GE" : ("Great Native Engineer"),
								"GM" : ("Great Native Merchant"),
								"GG" : ("Great Native General"),
								"GSPY" : ("Great Native Spy")
							},
							"CIVILIZATION_INDEPENDENT" :
							{
								"GP" : ("Great Independent Prophet"),
								"GA" : ("Great Independent Artist"),
								"GS" : ("Great Independent Scientist"),
								"GE" : ("Great Independent Engineer"),
								"GM" : ("Great Independent Merchant"),
								"GG" : ("Great Independent General"),
								"GSPY" : ("Great Independent Spy")
							},
							"CIVILIZATION_INDEPENDENT2" :
							{
								"GP" : ("Great Independent Prophet"),
								"GA" : ("Great Independent Artist"),
								"GS" : ("Great Independent Scientist"),
								"GE" : ("Great Independent Engineer"),
								"GM" : ("Great Independent Merchant"),
								"GG" : ("Great Independent General"),
								"GSPY" : ("Great Independent Spy")
							},
							"DEFAULT" :
							{
								"GP" : (),
								"GA" : (),
								"GS" : (),
								"GE" : (),
								"GM" : (),
								"GG" : (),
								"GSPY" : ()
							},
						}	



def generateCivilizationName(iCivilizationType, infoUnit):
	unitName = ""
	strCivilizationType = "DEFAULT"


	if(gc.getCivilizationInfo(iCivilizationType) != None):		
		strCivilizationType = gc.getCivilizationInfo(iCivilizationType).getType()

	strGPtype = ""

	if (infoUnit == gc.getInfoTypeForString("UNITCLASS_PROPHET")):
		strGPtype = "GP"

	if (infoUnit == gc.getInfoTypeForString("UNITCLASS_ARTIST")):
		strGPtype = "GA"

	if (infoUnit == gc.getInfoTypeForString("UNITCLASS_SCIENTIST")):
		strGPtype = "GS"

	if (infoUnit == gc.getInfoTypeForString("UNITCLASS_MERCHANT")):
		strGPtype = "GM"

	if (infoUnit == gc.getInfoTypeForString("UNITCLASS_ENGINEER")):
		strGPtype = "GE"

	if (infoUnit == gc.getInfoTypeForString("UNITCLASS_GREAT_GENERAL")):
		strGPtype = "GG"

	if (infoUnit == gc.getInfoTypeForString("UNITCLASS_GREAT_SPY")):
		strGPtype = "GSPY"


        # Main Naming Mechanism
	if (RandomNameOrder == 1):
                # Random Naming System
		if(len(civilizationNameHash[strCivilizationType][strGPtype]) > 0):
                        # Get random name
			randomCivName = gc.getGame().getMapRand().get(len(civilizationNameHash[strCivilizationType][strGPtype]), "Random Name")
			unitName = civilizationNameHash[strCivilizationType][strGPtype][randomCivName]
			
			# Remove the selected name from the main list, so we don't have duplicate great people born in one game
			newList1 = civilizationNameHash[strCivilizationType][strGPtype][0:randomCivName]
			newList2 = civilizationNameHash[strCivilizationType][strGPtype][(randomCivName + 1):len(civilizationNameHash[strCivilizationType][strGPtype])]
			civilizationNameHash[strCivilizationType][strGPtype] = newList1 + newList2
			
			return unitName

	if (RandomNameOrder == 0):
		# Sequential Naming System
		if(len(civilizationNameHash[strCivilizationType][strGPtype]) > 0):
                        # Pick the first name in the list
			unitName = civilizationNameHash[strCivilizationType][strGPtype][0]

                        # Remove the name from the list
			newList = civilizationNameHash[strCivilizationType][strGPtype][1:len(civilizationNameHash[strCivilizationType][strGPtype])]
			civilizationNameHash[strCivilizationType][strGPtype] = newList

			return unitName
	

	
