import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Random;

import sun.nio.cs.ext.ISCII91;

import weka.core.Instance;
import weka.core.Instances;
import weka.classifiers.trees.RandomForest;
import weka.filters.Filter;
import weka.filters.unsupervised.attribute.Remove;
import weka.classifiers.Evaluation;

class Main{


//Variables for Random Forest classification

public static RandomForest RF = new RandomForest();
public static Instances RF_trainingInstances;
public static Instances RF_testInstances;


public static void loadTrainingInstances(boolean verbose) {

    try {

        //Load training instances into data

        System.out.println("");

        System.out.println("Loading training instances into RandomForest classifier...");

        BufferedReader reader = new BufferedReader(

        new FileReader("/home/inge/Projects/Afstudeerproject/TrainingData_allbehaviours.arff"));
        

        Instances data = new Instances(reader);

        reader.close();

        // setting class attribute

        data.setClassIndex(0);           

        //Filter out timestamp string data

        RF_trainingInstances = data;   // apply filter
       


        //Build RandomForest classifier

        String[] options_RF = new String[1];

        options_RF[0] = "-D";          // debug output

        //RandomForest RF = new RandomForest(); //declared as public

        //RF.setOptions(options_RF);

        RF.buildClassifier(RF_trainingInstances);



        if (verbose) {

            //Get classification of example data

            //System.out.println(RF.toString());

            Evaluation eTest = new Evaluation(data);
            eTest.crossValidateModel(RF, data, 10, new Random());

            //eTest.evaluateModel(RF, RF_trainingInstances);



            // Print the result à la Weka explorer:

            String strSummary = eTest.toSummaryString();

            System.out.println(strSummary);



            // Get the confusion matrix

            //double[][] cmMatrix = eTest.confusionMatrix();                               

        }



        System.out.println("-done loading " + RF_trainingInstances.numInstances() + " training instance(s)");

    }

    catch (Exception e) {

        //Error reading file

        System.out.println("ERROR!!! - In function loadTrainingInstances()...");

        System.out.println("-" + e);

    }                           

}



public static void loadTestInstances(boolean verbose) {

    try {

        //Load test instances into data

        System.out.println("");

        System.out.println("Loading test instances...");

        BufferedReader reader = new BufferedReader(

        new FileReader("/home/inge/Projects/Afstudeerproject/TestData.arff"));

        Instances data = new Instances(reader);

        reader.close();

        // setting class attribute

        data.setClassIndex(0);        //2nd to last attribute is used for classification (last is timestamp)


        RF_testInstances = data;  // apply filter                                



        System.out.println("-done loading " + RF_testInstances.numInstances() + " test instance(s)");

    }

    catch (Exception e) {

        //Error reading file

        System.out.println("ERROR!!! - In function loadTestInstances()...");

        System.out.println("-" + e);

    }                           

}



public static Instance selectTestInstance() {

    //Select last instance from loaded set of Test Instances



    //Create test instance

    //Instance testInstance = new Instance(newDataTest.firstInstance());

    //Instance testInstance = new Instance(newDataTest.instance(0));

    Instance testInstance = new Instance(RF_testInstances.lastInstance());

    //System.out.println("-selecting last instance in test set RF_testInstances, done");



    // Specify that the instance belong to the training set

    // in order to inherit from the set description                               

    testInstance.setDataset(RF_trainingInstances);

    System.out.println("-selected last instance in test set: " + testInstance.toString() );



    return testInstance;

}



public static double classifyInstance(Instance testInstance, boolean verbose) {

    try {

        //Classify one particular instance from loaded set of Test Instances



        //Create test instance

        //Instance testInstance = new Instance(newDataTest.firstInstance());

        //Instance testInstance = new Instance(newDataTest.instance(0));

        //Instance testInstance = new Instance(RF_testInstances.lastInstance());

        //System.out.println("-selecting last instance in test set RF_testInstances, done");



        // Specify that the instance belong to the training set

        // in order to inherit from the set description                               

        //testInstance.setDataset(RF_trainingInstances);



        // Get the likelihood of each classes

        // fDistribution[0] is the probability of being “positive”

        // fDistribution[1] is the probability of being “negative”

        double[] fDistribution = RF.distributionForInstance(testInstance);



        if (verbose) {

            System.out.println("");

            System.out.println("Classifying selected test instance...");                              

            System.out.println("-probability of instance being appropriate     (1): " + fDistribution[1]);

            System.out.println("-probability of instance being non-appropriate (0): " + fDistribution[0]);

            System.out.println("-returning appropriateness probability of: " + fDistribution[1]);

        }



        return fDistribution[1];

    }

    catch (Exception e) {

        //Error reading file

        System.out.println("ERROR!!! - In function classifyInstance()...");

        System.out.println("-" + e);

        return 0.0; //dummy value

    }                           

}
public static void main(String[] args)
{
	loadTrainingInstances(true);
	//loadTestInstances(true);
	//Instance test = selectTestInstance();
	//for(int i = 0; i < RF_testInstances.numInstances(); i++)
	//{
	//	classifyInstance(RF_testInstances.instance(i), true);
	//}
		
}
	
}