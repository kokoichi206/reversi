#include <iostream>
#include <vector>

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

// 4＊4盤オセロの解析
#include <iostream>
#include <vector>

// 盤面が(bl, wh), 手番がcoである局面のスコア
int rec(int alpha, int beta, int bl, int wh, int co){
	//石の於ける場所を求める
	std::vector<int> mine, opp;
	for (int ce = 0; ce < 16; ++ce){
		if (put(bl, wh, co, ce))
			mine.push_back(ce);
		if (put(bl, wh, 1 - co, ce))
			opp.push_back(ce);
	}
	if (mine.empty() && opp.empty())
		return calc(bl, wh, co);
	
	// パスの場合
	if (main.empty())
		return -rec(-beta, -alpha, bl, wh, 1-co);

	// 各遷移を考える
	for (auto ce: mine){
		// 色を反転する
		int rev = put(bl, wh, co, ce);
		int bl2 = bl ^ rev, wh2 = wh ^ rev;

		// ceにおく
		if (co == BLACK) bl2 |= 1 << ce;
		else wh2 |= 1 << ce;

		// 遷移局面のスコアを符号反転して受け取り、値更新
		int score = -rec(-beta, -alpha, bl2, wh2, 1 - co);
		alpha = std::max(alpha, score);

		// βカット
		if (alpha >= beta) return alpha;
	}
	return alpha;
}

int main(){
	// 初期配置
	int bl = (1 << 6) | (1 << 9);
	int wh = (1 << 5) | (1 << 10);
	
	int score = rec(-16, 16, bl, wh, BLACK);
	std::cout << score << std::endl;
}
