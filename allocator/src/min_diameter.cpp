#include <bits/stdc++.h>
using namespace std;

int Diameter(vector<int> V, vector<vector<int> > l){
	int v_size = V.size();
	int diameter = 0;
	for(int i=0;i<v_size;i++){
		for(int j=i+1;j<v_size;j++){
			int u,v;
			u = V[i];
			v = V[j];
			diameter = max(l[u][v], diameter);
		}
	}
	return diameter;
}

vector<int> FindMinStar(vector<int> V, vector<int> w, vector<vector<int> > l, int v, int s){
	
	vector<int> V_;
	V_.push_back(v);

	int i = 1;
	int size = w[v];
	int j=0;
	vector<pair<int,int> > e;
	vector<int>::iterator it;
	for(it = l[v].begin(), j=0; it != l[v].end();it++,j++){
		int u = *it;
		e.push_back({l[v][u], j});
	}
	sort(e.begin(),e.end());

	while(size<s and i<e.size()){
		int ui = e[i].second;
		i = i + 1;
		if(find(V.begin(), V.end(), ui) == V.end() or ui==v)
			continue;
		V_.push_back(ui);
		size = size + w[ui];
	}

	if(size<s){
		vector<int> tmp;
		return tmp;
	}
	return V_;
}

vector<int> MinDiameterGraph(vector<int> V, vector<int> w, vector<vector<int> > l, int s){
	
	vector<int> G_;
	int min_diameter = INT_MAX;

	for(auto it=V.begin();it!=V.end();it++){
		int v = *it;
		vector<int> G__ = FindMinStar(V, w, l, v, s);
		if(Diameter(G__, l) < min_diameter){
			min_diameter = Diameter(G__, l);
			G_ = G__;
		}
	}
	return G_;
}

int main(int argc, char **argv){
	// if(argc<2){
	// 	printf("Usage: <path to executable> <required cores>\n");
	// 	exit(0);
	// }

	// int required_cores = atoi(argv[1]);
	// Currently hard coded
	int required_cores = 10;
	vector<int> active_nodes{0,1,2,3,4,5};
	vector<int> core_count{2,2,4,6,6,8};
	vector< vector<int> > inv_bandwidth;

	for(int i=0;i<6;i++){
		vector<int> tmp;
		for(int j=0;j<6;j++)
			tmp.push_back(rand()%100 +1);
		inv_bandwidth.push_back(tmp);
	}

	vector<int> G = MinDiameterGraph(active_nodes, core_count, inv_bandwidth, required_cores);
	for(auto it = G.begin(); it!=G.end();it++){
		cout<<*it<<" ";
	}
	cout<<endl;
	return 0;
}
