# coding: utf-8

from Core import *
from Files import *
from CityNameManager import *


LANGUAGE_NAMES = {
	iLangEgyptian: "Egyptian",
	iLangEgyptianArabic: "Egyptian_Arabic",
	iLangIndian: "Indian",
	iLangChinese: "Chinese",
	iLangTibetan: "Tibetan",
	iLangBabylonian: "Babylonian",
	iLangPersian: "Persian",
	iLangGreek: "Greek",
	iLangPhoenician: "Phoenician",
	iLangLatin: "Latin",
	iLangMayan: "Mayan",
	iLangJapanese: "Japanese",
	iLangEthiopian: "Ethiopian",
	iLangKorean: "Korean",
	iLangByzantine: "Byzantine",
	iLangNorse: "Norse",
	iLangArabian: "Arabian",
	iLangKhmer: "Khmer",
	iLangIndonesian: "Indonesian",
	iLangSpanish: "Spanish",
	iLangFrench: "French",
	iLangEnglish: "English",
	iLangGerman: "German",
	iLangRussian: "Russian",
	iLangDutch: "Dutch",
	iLangMalian: "Malian",
	iLangPolish: "Polish",
	iLangPortuguese: "Portuguese",
	iLangQuechua: "Quechua",
	iLangItalian: "Italian",
	iLangMongolian: "Mongolian",
	iLangAztec: "Aztec",
	iLangTurkish: "Turkish",
	iLangThai: "Thai",
	iLangCongolese: "Congolese",
	iLangPrussian: "Prussian",
	iLangAmerican: "American",
	iLangCeltic: "Celtic",
	iLangMexican: "Mexican",
	iLangPolynesian: "Polynesian",
	iLangHarappan: "Harappan",
}


def exportToCsv():
	rows = []
	
	for iLanguage in range(iNumLanguages):
		languageName = LANGUAGE_NAMES[iLanguage]
		
		for baseName, renameName in tRenames[iLanguage].items():
			rows.append((baseName, renameName, languageName))
	
	FileMap.write(rows, "Export/Extracted_City_Names_1.17.csv", bReverse=False)
