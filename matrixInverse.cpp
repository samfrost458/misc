// Matrix inverse
// reads in a 2D vector (matrix)
// finds the determinant (Leibniz formula, compuationally expensive) and prints if necessary
// finds the inverse, writes it in a new file
// reads and writes files where each value is separated by commas and lines
// prints intermediate steps to console if required

#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

// function to read in a file to a 2D array, with values separated by commas and lines
vector <vector<double> > matrixFileRead(string fileName, string fileExtension, char delim) {
    // declare variables
    vector <vector<double> > data;
    string x0, xn; // temporary string variables
    string line; // variable to hold each file line
    int comma; // location of comma (or other specified delim character)
    
    // input file
    string infilename = fileName + fileExtension;
    ifstream File (infilename);
    
    // read file into data matrix
    if (File.is_open()) {
        while (!File.eof() ) {
            getline(File, line);
            
            if (line.length() > 0) {
                // create temporary vector
                vector <double> temp;
                
                comma = line.find(delim,0);
                x0 = line.substr(0,comma);
                temp.push_back(atof(x0.c_str()));
                
                while (comma != string::npos) {
                    xn = line.substr(comma + 1,line.length()-comma-1);
                    temp.push_back(atof(xn.c_str()));
                    comma = line.find(delim,comma+1); // will return string::npos if comma not found
                }
                
                // push temporary vector onto data vector
                data.push_back(temp);
            }
        }
        
        File.close();
    } else {
        cerr << "Error: input file\n";
        exit(1);
    }
    return data;
}

// function to print a matrix
string print_matrix(vector< vector<double> > data, char delim) {
    // find number of rows and columns
    int rows = data.size();
    int columns = data[0].size();
    
    string output;
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < columns; j++) {
            output += to_string(data[i][j]);
            if (j < columns-1) {
                output += delim;
            }
        }
        output += "\n";
    }
    output += "\n";
    return output;
}

// function to find leviCivita cymbol of a set of numbers
int leviCivita(vector <int> permutations) {
    int epsilon = 1;
    for (int i = 0; i < permutations.size()-1; i++) {
        for (int j = 0; j < permutations.size(); j++) {
            if (j > i) {
                if (permutations[j] > permutations[i]) epsilon *= +1;
                if (permutations[j] < permutations[i]) epsilon *= -1;
                // else permutations[i] == permutations[j], leviCivita = 0
                //else return 0;
            }
        }
    }
    return epsilon;
}

// function to find determinant of a matrix (computationally expensive (O(n^2) time))
double determinant(vector < vector<double> > data, bool print = true) {
    // find number of rows and columns
    int rows = data.size();
    int columns = data[0].size();
    
    // if matrix is not square, cannot calculate determinant, exit program
    if (rows != columns) {
        cerr << "Error: matrix is not square, cannot calculate determinant" << endl;
        exit(1);
    }
    
    // array to hold 1, 2, 3, ..., rows for next_permutation() to act on
    vector <int> permutations;
    for (int i = 1; i < rows+1; i++) {
        permutations.push_back(i);
    }
    
    double sum = 0;
    do { // loop over all permutations to find terms in Leibniz formula
        double term = 1;
        for (int i = 0; i < rows; i++) {
            term *= data[ permutations[i]-1 ][i];
        }
        // for even/odd permutations, sign is +/- respectively
        int sign = leviCivita(permutations);
        sum += sign * term;
        
    } while (next_permutation(permutations.begin(), permutations.end()));
    
    if (print) cout << "Determinant: " << sum << endl;
    return sum;
}

// function to invert matrix (prints intermediate steps if wanted)
vector <vector<double> > invertMatrix(vector <vector<double> > data, bool print = false, char delim = ',') {
    // find number of rows and columns
    int rows = data.size();
    int columns = data[0].size();
    
    // as a test, reprint the matrix
    if (print) {
        cout << "Original matrix" << endl;
        cout << print_matrix(data, delim);
    }
    
    // if matrix is not square, cannot calculate inverse, exit program
    if (rows != columns) {
        cerr << "Error: matrix is not square, cannot calculate inverse" << endl;
        exit(1);
    }
    
    // if determinant is 0, cannot calculate inverse, exit program
    if (determinant(data, print) == 0) {
        cerr << "Error: matrix determinant is 0, cannot calculate inverse" << endl;
        exit(1);
    }
    
    // add identity matrix to data before elimination
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < columns; j++) {
            if (i == j) {
                data[i].push_back(1);
            }
            else {
                data[i].push_back(0);
            }
        }
    }
    // now number of columns should have doubled, recalculate
    columns = data[0].size();
    
    // as a test, reprint the matrix
    if (print) {
        cout << "With identity matrix" << endl;
        cout << print_matrix(data, delim);
    }
    
    double subtraction_coeff;
    double normaliser;
    
    // Gaussian elimination
    for (int i = 0; i < rows; i++) {
        normaliser = data[i][i];
        for (int j = 0; j < columns; j++) {
            data[i][j] = data[i][j] / normaliser;
        }
        for (int j = 0; j < rows-i-1; j++) {
            subtraction_coeff = data[rows-j-1][i];
            for (int k = 0; k < columns; k++) {
                data[rows-j-1][k] = data[rows-j-1][k] - data[i][k] * subtraction_coeff;
            }
        }
    }
    
    // as a test, reprint the matrix
    if (print) {
        cout << "After Gaussian elimination [row echelon form]" << endl;
        cout << print_matrix(data, delim);
    }
    
    // Back substitution
    for (int i = 0; i < rows-1; i++) {
        for (int j = 0; j < rows-i-1; j++) {
            subtraction_coeff = data[rows-j-i-2][rows-i-1];
            for (int k = 0; k < columns; k++) {
                data[rows-j-i-2][k] = data[rows-j-i-2][k] - data[rows-i-1][k] * subtraction_coeff;
            }
        }
    }
    
    // as a test, reprint the matrix
    if (print) {
        cout << "After back substitution" << endl;
        cout << print_matrix(data, delim);
    }
    
    // isolate the portion of this larger matrix containing the inverse into a new matrix called inverse
    vector< vector<double> > inverse;
    for (int i = 0; i < rows; i++) {
        vector< double > temp_inverse;
        for (int j = columns/2; j < columns; j++) {
            temp_inverse.push_back( data[i][j] );
        }
        inverse.push_back(temp_inverse);
    }
    
    // now number of columns should have halved again, recalculate
    columns = inverse[0].size();
    
    // print inverse
    if (print) {
        cout << "Inverse matrix" << endl;
        cout << print_matrix(inverse, delim);
    }
    
    return inverse;
}


int main() {
    string fileName      = "6by6";
    string fileExtension = ".txt";
    char delim = ',';
    bool print = true;
    
    // read in file to data array
    vector <vector<double> > data = matrixFileRead(fileName, fileExtension, delim);
    
    // find inverse
    vector <vector<double> > inverse = invertMatrix(data, print, delim);
    
    // write inverted matrix into a new text file
    string outfilename = fileName + "_inverse" + fileExtension;
    ofstream outFile (outfilename.c_str());
    if (outFile.is_open()) {
        outFile << print_matrix(inverse, delim);
        outFile.close();
    }
    else {
        cout << "Error: output file" << endl;
        exit(1);
    }
    
    return 0;
}
