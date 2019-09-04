#include <bits/stdc++.h>
#include <sqlite3.h>

using namespace std;

int NUM_HOSTS = 50;
#define DEBUG 1

map<string, vector<double> > allData;
vector< vector<double> > bandwidth;
string homedir = "/users/btech/akashish";

static int callback_node(void *NotUsed, int argc, char **argv, char **azColName) {
	for(int i = 0; i<argc; i++) {
		string field(azColName[i]);
		if(field=="node"){
			string s(argv[i]);
			allData[field].push_back( stoi(s.substr(5,s.length())) );
			continue;
		}
		allData[field].push_back(stod(argv[i]));
	}
	return 0;
}

static int callback_bw(void *NotUsed, int argc, char **argv, char **azColName) {
	int u,v;
	long double bw;
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


static int callback_latency(void *NotUsed, int argc, char **argv, char **azColName) {
	int u,v;
	long double bw;
	for(int i = 0; i<argc; i++) {
		string field(azColName[i]);
		if(field=="hostA")
			u = stoi(argv[i]);
		else if (field=="hostB")
			v = stoi(argv[i]);
		else if (field=="latency")
			bw = stod(argv[i]);
	}

	int uidx = find(allData["node"].begin(), allData["node"].end(), u) - allData["node"].begin();
	int vidx = find(allData["node"].begin(), allData["node"].end(), v) - allData["node"].begin();
	if (uidx!=NUM_HOSTS and vidx!=NUM_HOSTS){
		latency[uidx][vidx] = bw;
		latency[vidx][uidx] = bw;
	}

	if(uidx==vidx)
		latency[uidx][vidx] = 0;
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
		cout << "loop ";
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
	cout << "done";
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
	cout << "done";
	return 0;
}

int read_db_latency(string hostname, FILE* logfile){
	
	sqlite3* db = open_db(hostname, logfile);
	if(db == NULL)
		return SQLITE_CANTOPEN;
	char *zErrMsg = 0;
	int rc;
	
	// Get bandwidth data
	string sql = "SELECT * from latency";
	int err = exec_db(db, sql, &callback_latency, hostname, logfile);
	sqlite3_close(db);
	return 0;
}

	// // Read node data
	// for(int idx=0; idx<NUM_HOSTS; idx++){
	// 	int err = read_db(hostnames[idx], logfile);
	// 	if(err == SQLITE_CORRUPT or err==SQLITE_ERROR or err==SQLITE_CANTOPEN){
	// 		hostnames.erase(idx + hostnames.begin());
	// 		idx--;
	// 		NUM_HOSTS--;
	// 	}
	// }

	// // Read bandwidth data
	// for(int idx=0; idx<NUM_HOSTS; idx++){
	// 	int err1 = read_db_bw(hostnames[idx], logfile);
	// 	// int err2 = read_db_latency(hostnames[idx], logfile);
	// 	int flag1 = (err1 == SQLITE_CORRUPT or err1==SQLITE_ERROR or err1==SQLITE_CANTOPEN);
	// 	// int flag2 = (err2 == SQLITE_CORRUPT or err2==SQLITE_ERROR or err2==SQLITE_CANTOPEN);
	// 	if(flag1){
	// 		hostnames.erase(idx + hostnames.begin());
	// 		idx--;
	// 		NUM_HOSTS--;
	// 	}
	// }