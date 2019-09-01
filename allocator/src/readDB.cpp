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
        allData[azColName[i]].push_back( stod(s.substr(5,s.length())) );
        continue;
    }
    if(field=="memory_10" or field=="memory_50" or field=="memory_150" or field=="memory"){
        string s(argv[i]);
        allData[azColName[i]].push_back( stod(s.substr(0,s.length()-6)) );
        continue;
    }
      try{
        allData[azColName[i]].push_back(stod(argv[i]));
      }
      catch(...){

      }
   }
   return 0;
}

static int callback_bw(void *NotUsed, int argc, char **argv, char **azColName) {
   
   int u,v;
   double bw;
   for(int i = 0; i<argc; i++) {
    string field(azColName[i]);
    if(field=="HostA")
        u = stoi(argv[i]);
    else if (field=="HostB")
        v = stoi(argv[i]);
    else if (field=="bw"){
        cout<<"bw:"<<argv[i];
        bw = stod(argv[i]);
        cout<<"bw:"<<bw<<endl;
    }
   }
   u = find(allData["node"].begin(), allData["node"].end(), u) - allData["node"].begin();
   v = find(allData["node"].begin(), allData["node"].end(), v) - allData["node"].begin();
   bandwidth[u][v] = bw;
   return 0;
}

void read_db(string hostname, FILE* logfile){
    sqlite3 *db;
    char *zErrMsg = 0;
    int rc;

    string datadir = homedir + "/.eagle/" + hostname + "/data.db";
    rc = sqlite3_open(datadir.c_str(), &db);
    if( rc ) {
        fprintf(logfile, "Can't open database: %s\n", sqlite3_errmsg(db));
        return;
    } else {
        fprintf(logfile, "Opened database successfully\n");
    }

    // Get node data
    string node_sql = "SELECT * from node";
    rc = sqlite3_exec(db, node_sql.c_str(), callback_node, 0, &zErrMsg);

    if( rc != SQLITE_OK ){
        fprintf(logfile, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        fprintf(logfile, "Records read successfully\n");
    }

    // Get bandwidth data
    string bw_sql = "SELECT * from bw";
    rc = sqlite3_exec(db, bw_sql.c_str(), callback_bw, 0, &zErrMsg);

    if( rc != SQLITE_OK ){
        fprintf(logfile, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        fprintf(logfile, "BW records read successfully\n");
    }
    sqlite3_close(db);
}

void compute_power(double comp_power[], map<string, double> weights){
    for(int i=0;i<NUM_HOSTS;i++){
        map<string, double>::iterator it;
        for(it=weights.begin();it!=weights.end();it++){
            string key = it->first;
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
    weights.insert({"band_150", 2});
    weights.insert({"cpucount", 6});
    weights.insert({"cpufreqmax", 4});
    weights.insert({"cpucount", 6});

    weights.insert({"load_1", -2});
    weights.insert({"load_5", -7});
    weights.insert({"load_15", -5});

    weights.insert({"band_10", 2});
    weights.insert({"band_50", 6});
    weights.insert({"band_150", 6});

    weights.insert({"util_10", -4});
    weights.insert({"util_50", -7});

    weights.insert({"memory", 7});
    weights.insert({"memory_50", 5});
    weights.insert({"nodeusers",-5});
}

int main(){
    // Get list of hosts
    ifstream hostfile(homedir+"/.eagle/livehosts.txt");
    vector<string> hostnames;
    string hostname;
    while(hostfile >> hostname){
        hostnames.push_back(hostname);
    }
    NUM_HOSTS = hostnames.size();
    
    FILE *logfile;
    logfile = fopen("allocator.log","w");

    // Initialize bandwidth
    for(int i=0;i<NUM_HOSTS;i++){
        vector<double> tmp;
        for(int j=0;j<NUM_HOSTS;j++){
            tmp.push_back(INT16_MAX);
        }
        bandwidth.push_back(tmp);
    }

    auto start = time(NULL); 
    for(int idx=0; idx<NUM_HOSTS; idx++){
        read_db(hostnames[idx], logfile);
    }
    auto end = time(NULL); 
    auto duration = (end - start); 
    cout<<duration<<endl;

    map<string, vector<double> >::iterator it;
    for(it=allData.begin();it!=allData.end();it++){
        string field = it->first;
        // Normalize
        transform(allData[field].begin(), allData[field].end(), allData[field].begin(), bind2nd(divides<double>(), accumulate(allData[field].begin(), allData[field].end(), 0)));
        transform(allData[field].begin(), allData[field].end(), allData[field].begin(), bind2nd(multiplies<double>(), 100));
    }

    map<string, double> weights;
    set_weights(weights);

    // normalize
    double comp_power[NUM_HOSTS] = {0};
    compute_power(comp_power, weights);

    fclose(logfile);
    if(DEBUG){
        printData();
    }
    return 0;
}