#Hugh_Mann: This is just a simple wrapper for the founding city name maps; it pulls in all the language lists and puts in them in dFoundMaps;
#To avoid circular dependency issues, it also includes the language list that was previously in CityNameManager.py
#New paradigm is one m<Language>.py map file per language

from mEgyptian   import *
from mChinese    import *
from mBabylonian import *
from mGreek      import *
from mIndian     import *
from mPhoenician import *
from mPersian    import *
from mLatin      import *
from mEthiopian  import *
from mKorean     import *
from mMayan      import *
from mByzantine  import *
from mJapanese   import *
from mViking     import *
from mArabian    import *
from mTibetan    import *
from mKhmer      import *
from mIndonesian import *
from mSpanish    import *
from mFrench     import *
from mEnglish    import *
from mGerman     import *
from mRussian    import *
from mMalian     import *
from mPolish     import *
from mPortuguese import *
from mQuechua    import *
from mItalian    import *
from mMongolian  import *
from mAztec      import *
from mTurkish    import *
from mThai       import *
from mCongolese  import *
from mDutch      import *
from mPrussian   import *
from mAmerican   import *
from mMexican    import *
from mPolynesian import *
from mHarappan   import *

iNumLanguages = 41
(iLangEgyptian, iLangEgyptianArabic, iLangIndian, iLangChinese, iLangTibetan, 
iLangBabylonian, iLangPersian, iLangGreek, iLangPhoenician, iLangLatin, 
iLangJapanese, iLangEthiopian, iLangKorean, iLangMayan, iLangByzantine, 
iLangViking, iLangArabian, iLangKhmer, iLangIndonesian, iLangSpanish, 
iLangFrench, iLangEnglish, iLangGerman, iLangRussian, iLangDutch, 
iLangMalian, iLangPolish, iLangPortuguese, iLangQuechua, iLangItalian, 
iLangMongolian, iLangAztec, iLangTurkish, iLangThai, iLangCongolese, 
iLangPrussian, iLangAmerican, iLangCeltic, iLangMexican, iLangPolynesian,
iLangHarappan) = range(iNumLanguages)

dFoundMaps={iLangEgyptian:mEgyptian,iLangChinese:mChinese,iLangBabylonian:mBabylonian,iLangGreek:mGreek,iLangIndian:mIndian,\
iLangPhoenician:mPhoenician,iLangPersian:mPersian,iLangLatin:mLatin,iLangEthiopian:mEthiopian,iLangKorean:mKorean,iLangMayan:mMayan,\
iLangByzantine:mByzantine,iLangJapanese:mJapanese,iLangViking:mViking,iLangArabian:mArabian,iLangTibetan:mTibetan,iLangKhmer:mKhmer,\
iLangIndonesian:mIndonesian,iLangSpanish:mSpanish,iLangFrench:mFrench,iLangEnglish:mEnglish,iLangGerman:mGerman,iLangRussian:mRussian,\
iLangMalian:mMalian,iLangPolish:mPolish,iLangPortuguese:mPortuguese,iLangQuechua:mQuechua,iLangItalian:mItalian,iLangMongolian:mMongolian,\
iLangAztec:mAztec,iLangTurkish:mTurkish,iLangThai:mThai,iLangCongolese:mCongolese,iLangDutch:mDutch,iLangPrussian:mPrussian,iLangAmerican:mAmerican,\
iLangMexican:mMexican,iLangPolynesian:mPolynesian,iLangHarappan:mHarappan};