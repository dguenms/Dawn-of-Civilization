#pragma once

#ifndef SPAH_H
#define SPAH_H

//  <advc.250b> New class
class StartPointsAsHandicap {

class MajorCiv;

public:
	void setInitialItems();
	void rearrangeStartingPlots();
	void distribution(std::vector<int>& r) const;
	std::wstring* forSettingsScreen(bool bTab=true) const; // Exposed to Python through CvGame
	void write(FDataStreamBase* pStream);
	void read(FDataStreamBase* pStream);
	StartPointsAsHandicap();
	~StartPointsAsHandicap();


private:
	void reset();
	void gatherCivs();
	bool assignPoints();
	void assignAIPoints();
	void randomizePoints();
	void bounce(int i, int j);
	int minDist(CvPlot* p);
	void updatePointsDisplayString(bool bTab) const;
	/*int maxStartPoints(); // obsolete
	double meanStartPoints();*/
	static bool isLeftPtsLessThanRight(MajorCiv* left, MajorCiv* right);
	static bool isLeftCloserThanRight(MajorCiv* left, MajorCiv* right);

	std::vector<MajorCiv*> civs;
	int nCivs, nHuman;
	bool unequalDistrib;
	CvString report;
	mutable std::wstring* pointsDisplayString;

	// Serialized:
	 bool randPoints;
	 int allPts[2 * MAX_CIV_PLAYERS];

	// Wrapper for storing per-civ info
	class MajorCiv {

	public:
		MajorCiv(PlayerTypes civId);
		void setStartPoints_configured(int pts);
		void setStartPoints_actual(int pts);
		int startPoints_configured() const;
		int startPoints_actual() const;
		void setDist(int dist);
		int dist() const;
		int id() const;
		bool isHuman() const;
		CvPlot* startingPlot() const;
		// Modifying the wrapped civ
		 void assignStartPoints();
		 void assignStartingPlot(CvPlot* plot);

	private:
		int adjust(int pts);

		PlayerTypes civId;
		int startPoints_c, startPoints_a;
		bool actualPointsDone;
		static int foundingPrice;
		int d;
	};
};
// </advc.250b>

#endif
