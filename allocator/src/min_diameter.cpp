#include <bits/stdc++.h>
#include <sqlite3.h>

using namespace std;

int NUM_HOSTS;
#define DEBUG 1

map<string, vector<double> > allData;
vector< vector<double> > bandwidth;
vector<string> hostnames;

string homedir = "/users/btech/akashish";

static int callback_node(void *NotUsed, int argc, char **argv, char **azColName) {
	for(int i = 0; i<argc; i++) {
		string field(azColName[i]);
		if(field=="node"){
			string s(argv[i]);
			allData[field].push_back( stoi(s.substr(5,s.length())) );
			continue;
		}
		if(field=="memory_10" or field=="memory_50" or field=="memory_150" or field=="memory"){
			string s(argv[i]);
			allData[field].push_back( stod(s.substr(0,s.length()-6)) );
			continue;
		}
		allData[field].push_back(stod(argv[i]));
	}
	return 0;
}

static int callback_bw(void *NotUsed, int argc, char **argv, char **azColName) {
	int u,v;
	double bw;
	for(int i = 0; i<argc; i++) {
		string field(azColName[i]);
		if(field=="hostA")
			u = stoi(argv[i]);
		else if (field=="hostB")
			v = stoi(argv[i]);
		else if (field=="bw")
			bw = stod(argv[i]);
	}

	int uidx = find(allData["node"].begin(), allData["node"].end(), u) - allData["node"].begin();
	int vidx = find(allData["node"].begin(), allData["node"].end(), v) - allData["node"].begin();
	if (uidx!=NUM_HOSTS and vidx!=NUM_HOSTS){
		bandwidth[uidx][vidx] = bw;
		bandwidth[vidx][uidx] = bw;
	}

	if(uidx==vidx)
		bandwidth[uidx][vidx] = 0;
	return 0;
}

sqlite3* open_db(string hostname, FILE* logfile){
	sqlite3 *db;
	char *zErrMsg = 0;
	int rc;

	string datadir = homedir + "/.eagle/" + hostname + "/data.db";
	rc = sqlite3_open(datadir.c_str(), &db);
	if( rc ) {
		fprintf(logfile, "Can't open database for %s: %s %d\n",hostname.c_str(), sqlite3_errmsg(db), rc);
		return NULL;
	} else {
		fprintf(logfile, "Opened database successfully %s\n", hostname.c_str());
	}
	return db;
}

int exec_db(sqlite3* db, string sql, int (*callback)(void *NotUsed, int argc, char **argv, char **azColName), string hostname, FILE* logfile){
	char *zErrMsg = 0;
	int rc;

	rc = sqlite3_exec(db, sql.c_str(), callback, 0, &zErrMsg);
	if(rc == SQLITE_CORRUPT or rc==SQLITE_ERROR){
		return rc;
	}
	while(rc!=SQLITE_OK){
		rc = sqlite3_exec(db, sql.c_str(), callback, 0, &zErrMsg);
	}
	if( rc != SQLITE_OK ){
		fprintf(logfile, "SQL error for %s: %s %d\n",hostname.c_str(), zErrMsg, rc);
		
		sqlite3_free(zErrMsg);
	} else {
		fprintf(logfile, "Records read successfully for %s\n", hostname.c_str());
	}
}

int read_db(string hostname, FILE* logfile){
	sqlite3* db = open_db(hostname, logfile);
	if(db==NULL)
		return SQLITE_CANTOPEN;
	char *zErrMsg = 0;
	int rc;

	// Get node data
	string sql = "SELECT * from node";
	int err = exec_db(db, sql, &callback_node, hostname, logfile);
	sqlite3_close(db);
	return err;
}


int read_db_bw(string hostname, FILE* logfile){
	
	sqlite3* db = open_db(hostname, logfile);
	if(db == NULL)
		return SQLITE_CANTOPEN;
	char *zErrMsg = 0;
	int rc;
	
	// Get bandwidth data
	string sql = "SELECT * from bw";
	int err = exec_db(db, sql, &callback_bw, hostname, logfile);
	sqlite3_close(db);
	return 0;
}

void compute_power(double comp_power[], map<string, double> weights){
	for(int i=0;i<NUM_HOSTS;i++){
		map<string, double>::iterator it;
		for(it=weights.begin();it!=weights.end();it++){
			string key = it->first;
			if(weights[key]<0){
				comp_power[i] += (-weights[key])*(1-allData[key][i]);
			}
			else	
				comp_power[i] += weights[key]*allData[key][i];
		}
	}
	transform(comp_power,comp_power+NUM_HOSTS , comp_power, bind2nd(divides<double>(), accumulate(comp_power, comp_power+NUM_HOSTS, 0)));
	
	if(DEBUG)
	{
		for(int idx=0;idx<NUM_HOSTS;idx++)
			cout<<comp_power[idx]<<" ";
		cout<<endl;
	}
}

void printData(){
	cout<<"Printing bandwidth info:\n";
	for(int i=0;i<NUM_HOSTS;i++){
		for(int j=0;j<NUM_HOSTS;j++)
			cout<<bandwidth[i][j]<<" ";
		cout<<endl;
	}
}

void set_weights(map<string, double> &weights){

	weights.insert({"cpucount", 2});
	weights.insert({"cpufreqmax", 2});
	weights.insert({"cpucount", 2});

	weights.insert({"load_1", -2});
	weights.insert({"load_5", -2});
	weights.insert({"load_15", -2});

	weights.insert({"band_10", -8});
	weights.insert({"band_50", -7});
	weights.insert({"band_150", -6});

	weights.insert({"util_10", -2});
	weights.insert({"util_50", -2});

	weights.insert({"memory", 2});
	weights.insert({"memory_50", 2});
	weights.insert({"nodeusers",-7});
}

int Diameter(vector<int> V, vector<vector<double> > l){
	int v_size = V.size();
	int diameter = 0;
	for(int i=0;i<v_size;i++){
		for(int j=i+1;j<v_size;j++){
			int u,v;
			u = V[i];
			v = V[j];
			diameter = max(l[u][v], double(diameter));
		}
	}
	return diameter;
}

vector<int> FindMinStar(vector<int> V, vector<int> w, vector<vector<double> > l, int v, int s){
	
	vector<int> V_;
	V_.push_back(v);

	int i = 1;
	int size = w[v];
	int j=0;
	vector<pair<double,int> > e;
	vector<double>::iterator it;
	for(it = l[v].begin(), j=0; it != l[v].end();it++,j++){
		int u = *it;
		e.push_back({l[v][u], j});
	}
	sort(e.begin(),e.end(), greater<pair<double, int> >());

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

double compute_Comp(vector<int> G, double comp_power[]){
	double power = 0;
	for(int i=0;i<G.size();i++){
		power += comp_power[G[i]];
	}
	return power;
}

double compute_Netw(vector<int> G){
	double power = 0;
	for(int i=0;i<G.size();i++){
		for(int j=i+1;j<G.size();j++){
			power += bandwidth[G[i]][G[j]];
		}
	}
	if(G.size()==1)
		return 0;
	power /= (G.size()*G.size())/2;
	return power;
}

vector<int> MinDiameterGraph(vector<int> G, vector<int> w, vector<vector<double> > l, int s, double comp_power[]){
	
	vector<int> G_;
	int min_diameter = INT_MAX;
	double comp[NUM_HOSTS] = {0};
	double netw[NUM_HOSTS] = {0};
	double total_power[NUM_HOSTS] = {0};

	// Calculate compute and network power
	for(auto it=G.begin();it!=G.end();it++){
		int v = int(*it);
		vector<int> G__ = FindMinStar(G, w, l, v, s);
		if (G__.size()==0){
			continue;
		}
		comp[v] = compute_Comp(G__, comp_power);
		netw[v] = compute_Netw(G__);
	}

	// Normalize it
	transform(comp, comp + NUM_HOSTS, comp, bind2nd(divides<double>(), accumulate(comp, comp+NUM_HOSTS, 0.0)));
	transform(netw, netw + NUM_HOSTS, netw, bind2nd(divides<double>(), accumulate(netw, netw+NUM_HOSTS, 0.0)));

	// Compute total power
	int max_idx = 0;
	double max_pow = -1;
	for(int i=0;i<NUM_HOSTS;i++){
		total_power[i] = 0.2*comp[i] + 0.8*netw[i];
		if(DEBUG)
		if(total_power[i] > max_pow){
			max_pow = total_power[i];
			max_idx = i;
		}
	}

	if(DEBUG){
		cout<<"Computation, Network and Total power for each node:\n"<<endl;
		for(int i=0;i<NUM_HOSTS;i++){
			cout<<allData["node"][i]<<" "<<comp[i]<<" "<<netw[i]<<" "<<total_power[i]<<endl;
		}
		cout<<"Max:"<<max_pow<<" "<<allData["node"][max_idx]<<endl;
	}

	G_ = FindMinStar(G, w, l, max_idx, s);
	return G_;
}

void getLiveHosts(string filename){
	ifstream hostfile(filename);
	string hostname;
	while(hostfile >> hostname){
		cout<<hostname<<" ";
		hostnames.push_back(hostname);
	}
	NUM_HOSTS = hostnames.size();
	cout<<endl<<"Number of hosts: "<<NUM_HOSTS<<endl;
}

int main(int argc, char **argv){
	if(argc<3){
		cout<<"Usage: <executable> <number of hosts> <ppn>"<<endl;
		exit(0);
	}

	int required_cores = atoi(argv[1]);
	int ppn  = atoi(argv[2]);

	// Get list of hosts
	getLiveHosts(homedir+"/.eagle/livehosts.txt");
	
	FILE *logfile;
	logfile = fopen("allocator.log","w");

	// Initialize bandwidth
	for(int i=0;i<NUM_HOSTS;i++){
		vector<double> tmp;
		for(int j=0;j<NUM_HOSTS;j++){
			tmp.push_back(0);
		}
		bandwidth.push_back(tmp);
	}

	auto start = time(NULL); 
	
	// Read node data
	for(int idx=0; idx<NUM_HOSTS; idx++){
		int err = read_db(hostnames[idx], logfile);
		if(err == SQLITE_CORRUPT or err==SQLITE_ERROR or err==SQLITE_CANTOPEN){
			hostnames.erase(idx + hostnames.begin());
			idx--;
			NUM_HOSTS--;
		}
	}

	// Read bandwidth data
	for(int idx=0; idx<NUM_HOSTS; idx++){
		int err = read_db_bw(hostnames[idx], logfile);
		if(err == SQLITE_CORRUPT or err==SQLITE_ERROR or err==SQLITE_CANTOPEN){
			hostnames.erase(idx + hostnames.begin());
			idx--;
			NUM_HOSTS--;
		}
	}
	
	auto end = time(NULL); 
	auto duration = (end - start); 
	if(DEBUG)
		cout<<endl<<"Duration: "<<duration<<endl;
	
	// Normalize node data
	map<string, vector<double> >::iterator it;
	for(it=allData.begin();it!=allData.end();it++){
		string field = it->first;
		if(field=="node" or field=="corecount")
			continue;
		// Normalize
		transform(allData[field].begin(), allData[field].end(), allData[field].begin(), bind2nd(divides<double>(), accumulate(allData[field].begin(), allData[field].end(), 0)));
	}

	if(DEBUG){
		printData();
	}
	
	for(int i=0;i<NUM_HOSTS;i++){
		allData["corecount"][i] = ppn;
	}

	vector<int> active_nodes;
	vector<int> core_count;

	for(int i=0;i<NUM_HOSTS;i++)
		core_count.push_back(int(allData["corecount"][i]));
	for(int i=0;i<NUM_HOSTS;i++)
		active_nodes.push_back(i);

	if(DEBUG){
		cout<<endl<<"Nodes"<<endl;
		for(int i=0;i<NUM_HOSTS;i++){
			cout<<allData["node"][i]<<" ";
		}
		cout<<endl;
		for(int i=0;i<NUM_HOSTS;i++){
			cout<<hostnames[i]<<" ";
		}
		cout<<endl;
	}

	map<string, double> weights;
	set_weights(weights);
	double comp_power[NUM_HOSTS] = {0};
	compute_power(comp_power, weights);

	vector<int> G = MinDiameterGraph(active_nodes, core_count, bandwidth, required_cores, comp_power);

	if(G.size()==0)
		cout<<"Not found\n";
	
	FILE *hosts;
	hosts = fopen("hosts","w");
	if(DEBUG){
		for(auto it = G.begin(); it!=G.end();it++){
			cout<<allData["node"][*it]<<" "<<allData["corecount"][*it]<<endl;
			fprintf(hosts, "csews%d\n", int(allData["node"][*it]));
		}
		cout<<endl;
	}

	fclose(hosts);
	fclose(logfile);
	return 0;
}
