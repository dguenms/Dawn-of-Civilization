#include "CvGameCoreDLL.h"
#include "CvDiploParameters.h"
#include "CvGamePlay.h"
#include "FVariableSystem.h" // advc (moved from header)


CvDiploParameters::CvDiploParameters(PlayerTypes ePlayer) :
	m_eWhoTalkingTo(ePlayer),
	m_eCommentType(NO_DIPLOCOMMENT),
	m_bRenegotiate(false),
	m_bAIContact(false),
	m_bPendingDelete(false),
	m_iData(-1),
	m_bHumanDiplo(false),
	m_bOurOffering(false),
	m_bTheirOffering(false)
{
	/*m_ourOffer.clear();
	m_theirOffer.clear();*/ // advc: no need
}

CvDiploParameters::~CvDiploParameters()
{
	/*m_ourOffer.clear();
	m_theirOffer.clear();*/ // advc
}

void CvDiploParameters::setWhoTalkingTo(PlayerTypes eWhoTalkingTo)
{
	m_eWhoTalkingTo = eWhoTalkingTo;
}

PlayerTypes CvDiploParameters::getWhoTalkingTo() const
{	/*  <advc.134a> When checking a peace offer, the EXE calls this function
		shortly before an (erroneous) at-war check. Tell the recipient of the offer
		to feign peace. */
	CvTeam& kActiveTeam = GET_TEAM(GC.getGame().getActiveTeam());
	if(kActiveTeam.isPeaceOfferStage(1, TEAMID(m_eWhoTalkingTo)))
		kActiveTeam.advancePeaceOfferStage(TEAMID(m_eWhoTalkingTo));
	// </advc.134a>
	return m_eWhoTalkingTo;
}

void addVar(std::vector<FVariable>& argsList, const wchar *arg)
{
	if (arg)
	{
		FVariable var;
		var.m_eType = FVARTYPE_WSTRING;
		var.m_wszValue = new wchar[wcslen(arg)+1];
		wcscpy(var.m_wszValue, arg);
		argsList.push_back(var);
	}
}

void addVar(std::vector<FVariable>& argsList, int arg)
{
	if (arg != MAX_INT)
	{
		FVariable var;
		var.m_eType = FVARTYPE_INT;
		var.m_iValue = arg;
		argsList.push_back(var);
	}
}

#define SET_DIPLO_COMMENT_ARGS \
{ \
	std::vector<FVariable> argsList; \
	addVar(argsList, arg1); \
	addVar(argsList, arg2); \
	addVar(argsList, arg3); \
	setDiploComment(eCommentType, argsList.size() ? &argsList : NULL); \
}

void CvDiploParameters::setDiploComment(DiploCommentTypes eCommentType, CvWString  arg1, CvWString  arg2, CvWString  arg3)
SET_DIPLO_COMMENT_ARGS

void CvDiploParameters::setDiploComment(DiploCommentTypes eCommentType, CvWString  arg1, CvWString  arg2, int arg3)
SET_DIPLO_COMMENT_ARGS

void CvDiploParameters::setDiploComment(DiploCommentTypes eCommentType, CvWString  arg1, int arg2, CvWString  arg3)
SET_DIPLO_COMMENT_ARGS

void CvDiploParameters::setDiploComment(DiploCommentTypes eCommentType, CvWString  arg1, int arg2, int arg3)
SET_DIPLO_COMMENT_ARGS

void CvDiploParameters::setDiploComment(DiploCommentTypes eCommentType, int arg1, CvWString  arg2, CvWString  arg3)
SET_DIPLO_COMMENT_ARGS

void CvDiploParameters::setDiploComment(DiploCommentTypes eCommentType, int arg1, CvWString  arg2, int arg3)
SET_DIPLO_COMMENT_ARGS

void CvDiploParameters::setDiploComment(DiploCommentTypes eCommentType, int arg1, int arg2, CvWString  arg3)
SET_DIPLO_COMMENT_ARGS

void CvDiploParameters::setDiploComment(DiploCommentTypes eCommentType, int arg1, int arg2, int arg3)
SET_DIPLO_COMMENT_ARGS

void CvDiploParameters::setDiploComment(DiploCommentTypes eCommentType,
	std::vector<FVariable> const* pArgs)
{
	m_eCommentType = eCommentType;
	if (pArgs != NULL)
		m_diploCommentArgs = *pArgs;
}

void CvDiploParameters::setOurOfferList(CLinkList<TradeData> const& kOurOffer)
{
	m_ourOffer.clear();
	FOR_EACH_TRADE_ITEM(kOurOffer)
		m_ourOffer.insertAtEnd(*pItem);
}

const CLinkList<TradeData>& CvDiploParameters::getOurOfferList() const
{
	return m_ourOffer;
}

void CvDiploParameters::setTheirOfferList(CLinkList<TradeData> const& kTheirOffer)
{
	m_theirOffer.clear();
	FOR_EACH_TRADE_ITEM(kTheirOffer)
		m_theirOffer.insertAtEnd(*pItem);
}

CLinkList<TradeData> const& CvDiploParameters::getTheirOfferList() const
{
	return m_theirOffer;
}

void CvDiploParameters::setRenegotiate(bool bValue)
{
	m_bRenegotiate = bValue;
}
/*  advc.003j (comment): m_bRenegotiate is never set, and while the EXE calls
	getRenegotiate, it doesn't seem to matter if true or false is returned. */
bool CvDiploParameters::getRenegotiate() const
{
	return m_bRenegotiate;
}

void CvDiploParameters::setAIContact(bool bValue)
{
	m_bAIContact = bValue;
}

bool CvDiploParameters::getAIContact() const
{
	return m_bAIContact;
}


void CvDiploParameters::setPendingDelete(bool bPending)
{
	m_bPendingDelete = bPending;
}

bool CvDiploParameters::getPendingDelete() const
{
	return m_bPendingDelete;
}


void CvDiploParameters::setData(int iData)
{
	m_iData = iData;
}

int CvDiploParameters::getData() const
{
	return m_iData;
}

void CvDiploParameters::setHumanDiplo(bool bValue)
{
	m_bHumanDiplo = bValue;
}

bool CvDiploParameters::getHumanDiplo() const
{
	return m_bHumanDiplo;
}

void CvDiploParameters::setOurOffering(bool bValue)
{
	m_bOurOffering = bValue;
}

bool CvDiploParameters::getOurOffering() const
{
	return m_bOurOffering;
}

void CvDiploParameters::setTheirOffering(bool bValue)
{
	m_bTheirOffering = bValue;
}

bool CvDiploParameters::getTheirOffering() const
{
	return m_bTheirOffering;
}

void CvDiploParameters::setChatText(const wchar* szText)
{
	m_szChatText = szText;
}

const wchar* CvDiploParameters::getChatText() const
{
	return m_szChatText;
}

void CvDiploParameters::read(FDataStreamBase& stream)
{
	uint uiFlag;
	stream.Read(&uiFlag);

	int iType;
	stream.Read(&iType);
	m_eWhoTalkingTo = (PlayerTypes)iType;
	stream.Read(&iType);
	m_eCommentType = (DiploCommentTypes)iType;
	m_ourOffer.Read(&stream);
	m_theirOffer.Read(&stream);
	stream.Read(&m_bRenegotiate);
	stream.Read(&m_bAIContact);
	stream.Read(&m_iData);
	stream.Read(&m_bHumanDiplo);
	stream.Read(&m_bOurOffering);
	stream.Read(&m_bTheirOffering);
	stream.ReadString(m_szChatText);

	// read diplo args vec
	int iSize;
	stream.Read(&iSize);
	m_diploCommentArgs.resize(iSize);
	for (int i = 0; i < iSize; i++)
		m_diploCommentArgs[i].Read(&stream);
}

void CvDiploParameters::write(FDataStreamBase& stream) const
{
	uint uiFlag = 0;
	stream.Write(uiFlag);

	stream.Write(m_eWhoTalkingTo);
	stream.Write(m_eCommentType);
	m_ourOffer.Write(&stream);
	m_theirOffer.Write(&stream);
	stream.Write(m_bRenegotiate);
	stream.Write(m_bAIContact);
	stream.Write(m_iData);
	stream.Write(m_bHumanDiplo);
	stream.Write(m_bOurOffering);
	stream.Write(m_bTheirOffering);
	stream.WriteString(m_szChatText);

	// write diplo args vec
	int iSize = m_diploCommentArgs.size();
	stream.Write(iSize);
	for (int i = 0; i < iSize; i++)
		m_diploCommentArgs[i].Write(&stream);
}
