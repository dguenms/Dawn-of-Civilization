#pragma once
#ifndef CVDIPLOPARAMETERS_H
#define CVDIPLOPARAMETERS_H

#include "LinkedList.h"
//#include "CvStructs.h"
#include "FVariableSystem.h"

class CvDiploParameters
{
public:
	DllExport CvDiploParameters(PlayerTypes ePlayer);
	DllExport virtual ~CvDiploParameters();

	DllExport void setWhoTalkingTo(PlayerTypes eWhoTalkingTo);
	DllExport PlayerTypes getWhoTalkingTo() const;
	DllExport void setDiploComment(DiploCommentTypes eCommentType, const std::vector<FVariable>* args=NULL);

	// allow 3 args either int or string.  can't really use va_argslist here
	DllExport void setDiploComment(DiploCommentTypes eCommentType, CvWString  arg1, CvWString  arg2="", CvWString  arg3="");
	DllExport void setDiploComment(DiploCommentTypes eCommentType, CvWString  arg1, CvWString  arg2, int arg3=MAX_INT);
	DllExport void setDiploComment(DiploCommentTypes eCommentType, CvWString  arg1, int arg2, CvWString  arg3="");
	DllExport void setDiploComment(DiploCommentTypes eCommentType, CvWString  arg1, int arg2, int arg3=MAX_INT);
	DllExport void setDiploComment(DiploCommentTypes eCommentType, int arg1, CvWString  arg2="", CvWString  arg3="");
	DllExport void setDiploComment(DiploCommentTypes eCommentType, int arg1, CvWString  arg2, int arg3=MAX_INT);
	DllExport void setDiploComment(DiploCommentTypes eCommentType, int arg1, int arg2=MAX_INT, CvWString  arg3="");
	DllExport void setDiploComment(DiploCommentTypes eCommentType, int arg1, int arg2, int arg3=MAX_INT);

	DllExport DiploCommentTypes getDiploComment() const;
	DllExport void setOurOfferList(const CLinkList<TradeData>& ourOffer);
	DllExport const CLinkList<TradeData>& getOurOfferList() const;
	DllExport void setTheirOfferList(const CLinkList<TradeData>& theirOffer);
	DllExport const CLinkList<TradeData>& getTheirOfferList() const;
	DllExport void setRenegotiate(bool bValue);
	DllExport bool getRenegotiate() const;
	DllExport void setAIContact(bool bValue);
	DllExport bool getAIContact() const;
	DllExport void setPendingDelete(bool bPending);
	DllExport bool getPendingDelete() const;
	DllExport void setData(int iData);
	DllExport int getData() const;
	DllExport void setHumanDiplo(bool bValue);
	DllExport bool getHumanDiplo() const;
	DllExport void setOurOffering(bool bValue);
	DllExport bool getOurOffering() const;
	DllExport void setTheirOffering(bool bValue);
	DllExport bool getTheirOffering() const;
	DllExport void setChatText(const wchar* szText);
	DllExport const wchar* getChatText() const;
	DllExport const std::vector<FVariable>& getDiploCommentArgs() const { return m_diploCommentArgs; }

	DllExport void read(FDataStreamBase& stream);
	DllExport void write(FDataStreamBase& stream) const;

private:
	PlayerTypes m_eWhoTalkingTo;
	DiploCommentTypes m_eCommentType;
	CLinkList<TradeData> m_ourOffer;
	CLinkList<TradeData> m_theirOffer;
	bool m_bRenegotiate;
	bool m_bAIContact;
	bool m_bPendingDelete;
	int m_iData;
	bool m_bHumanDiplo;
	bool m_bOurOffering;
	bool m_bTheirOffering;
	CvWString m_szChatText;
	std::vector<FVariable> m_diploCommentArgs;
};

#endif