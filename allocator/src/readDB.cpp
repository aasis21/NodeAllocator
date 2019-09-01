#include <bits/stdc++.h>
#include <sqlite3.h>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>

using namespace std;
struct passwd *pw = getpwuid(getuid());

string homedir = pw->pw_dir;

static int callback(void *NotUsed, int argc, char **argv, char **azColName) {
   int i;
   for(i = 0; i<argc; i++) {
      printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
   }
   printf("\n");
   return 0;
}

int main(){
    // Get list of active hosts
    vector<string> hostnames;
    hostnames.push_back("csews12");

    for(int idx=0;idx<hostnames.size();idx++){
        sqlite3 *db;
        char *zErrMsg = 0;
        int rc;
        string datadir = homedir + "/.eagle/" + hostnames[idx] + "/data.db";
        rc = sqlite3_open(datadir.c_str(), &db);
        if( rc ) {
            fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
            return(0);
        } else {
            fprintf(stderr, "Opened database successfully\n");
        }
        string sql = "SELECT * from latency";
        rc = sqlite3_exec(db, sql.c_str(), callback, 0, &zErrMsg);
   
        if( rc != SQLITE_OK ){
            fprintf(stderr, "SQL error: %s\n", zErrMsg);
            sqlite3_free(zErrMsg);
        } else {
            fprintf(stdout, "Records created successfully\n");
        }
    
        sqlite3_close(db);
    }
    return 0;
}