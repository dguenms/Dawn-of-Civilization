#pragma once
#ifndef CVDIPLOPARAMETERS_H
#define CVDIPLOPARAMETERS_H

class FVariable;

class CvDiploParameters /* advc.003k: */ : private boost::noncopyable
{
public:
	DllExport CvDiploParameters(PlayerTypes ePlayer);
	virtual ~CvDiploParameters();

	DllExport void setWhoTalkingTo(PlayerTypes eWhoTalkingTo);
	DllExport PlayerTypes getWhoTalkingTo() const;

	void setDiploComment(DiploCommentTypes eCommentType,
			std::vector<FVariable> const* pArgs = NULL);

	// allow 3 args either int or string.  can't really use va_argslist here
	void setDiploComment(DiploCommentTypes eCommentType, CvWString  arg1, CvWString  arg2="", CvWString  arg3="");
	void setDiploComment(DiploCommentTypes eCommentType, CvWString  arg1, CvWString  arg2, int arg3=MAX_INT);
	void setDiploComment(DiploCommentTypes eCommentType, CvWString  arg1, int arg2, CvWString  arg3="");
	void setDiploComment(DiploCommentTypes eCommentType, CvWString  arg1, int arg2, int arg3=MAX_INT);
	void setDiploComment(DiploCommentTypes eCommentType, int arg1, CvWString  arg2="", CvWString  arg3="");
	void setDiploComment(DiploCommentTypes eCommentType, int arg1, CvWString  arg2, int arg3=MAX_INT);
	void setDiploComment(DiploCommentTypes eCommentType, int arg1, int arg2=MAX_INT, CvWString  arg3="");
	void setDiploComment(DiploCommentTypes eCommentType, int arg1, int arg2, int arg3=MAX_INT);

	DllExport DiploCommentTypes getDiploComment() const
	{
		return m_eCommentType;
	}
	DllExport void setOurOfferList(CLinkList<TradeData> const& kOurOffer);
	DllExport const CLinkList<TradeData>& getOurOfferList() const;
	DllExport void setTheirOfferList(CLinkList<TradeData> const& kTheirOffer);
	DllExport CLinkList<TradeData> const& getTheirOfferList() const;
	void setRenegotiate(bool bValue);
	DllExport bool getRenegotiate() const;
	void setAIContact(bool bValue);
	DllExport bool getAIContact() const;
	DllExport void setPendingDelete(bool bPending);
	DllExport bool getPendingDelete() const;
	void setData(int iData);
	DllExport int getData() const;
	DllExport void setHumanDiplo(bool bValue);
	DllExport bool getHumanDiplo() const;
	DllExport void setOurOffering(bool bValue);
	DllExport bool getOurOffering() const;
	DllExport void setTheirOffering(bool bValue);
	DllExport bool getTheirOffering() const;
	DllExport void setChatText(const wchar* szText);
	DllExport const wchar* getChatText() const;
	/*	advc.003k (note): Unused. I don't know how the EXE accesses
		m_diploCommentArgs; not through read/write either. memcopy I guess? */
	std::vector<FVariable> const& getDiploCommentArgs() const { return m_diploCommentArgs; }
	/*	advc (note): These two get called externally when a human-to-human trade
		is offered in a hotseat game. They get called internally when creating a savegame. */
	DllExport void read(FDataStreamBase& stream);
	DllExport void write(FDataStreamBase& stream) const;

private: /*	advc.003k (warning): It's not safe to add data members to this class,
			nor to rearrange the existing members! */
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

BOOST_STATIC_ASSERT(sizeof(CvDiploParameters) == 100); // advc.003k

#endif
