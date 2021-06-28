// 色
const int BLACK = 1, WHITE = 0;

// マスceを方向dに動かした結果を求める
std::vector<int> dx = {1, 0, -1, 0, 1, 1, -1, -1};
std::vector<int> dy = {0, 1, 0, -1, 1, -1, -1, 1};
int move(int ce, int d){
	int x = ce / 4 + dx[d], y = ce % 4 + dy[d];

	// 盤外に出る場合は-1とする
	if (x < 0 || x >= 4 || y < 0 || y >= 4)
		return -1;
	else
		return x * 4 + y;
}

// 盤面が(bl, wh)のとき、マスceの色がcoかどうか
bool iscolor(int bl, int wh, int co, int ce){
	if (ce == -1) return false;
	if (co == BLACK) return ((bl >> ce) & 1);
	else return ((wh >> ce) & 1);
}

// 盤面が(bl, wh)のとき、ますceに色coの石をおく
// 反転するますを返す（おけない時は0を返す）
int put(int bl, int wh, int co, int ce){
	if (((bl | wh) >> ce) & 1) return 0;
	int result = 0;
	for (int d = 0; d < 8; ++d){
		int rev = 0;
		int ce2 = move(ce, d);
		while(iscolor(bl, wh, 1 - co, ce2)) {
			rev |= 1 << ce2;
			ce2 = move(ce2, d);
		}
		if (iscolor(bl, wh, co, ce2))
			retult |= rev;
	}
	return result;
}

// 終局時のスコア計算
int calc(int bl, int wh, int co){
	int nbl = 0, nwh = 0, nem = 0;
	for (int ce = 0; ce < 16; ++ce){
		if ((bl >> ce) & 1) ++nbl;
		else if ((wh >> ce) & 1) ++nwh;
		else ++nem;
	}
	// 勝利側に空きますの個数を計算
	if (nbl > nwh) nbl += nem;
	else if (nbl < nwh) nwh += nem;
	// スコア
	if (co == BLACK) return nbl - nwh;
	else return nwh - nbl;
}
