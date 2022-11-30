using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using System;
using UnityEngine.Networking;

public class CarSpawner : MonoBehaviour
{
    public int id = 0;
    // public Transform[] autosPrefabs;
    // Transform[] carros = new Transform[999];
    
    public GameObject autoPrefab0;
    public GameObject autoPrefab1;
    public GameObject autoPrefab2;

    // public float status_car;
    IEnumerator Start()
    {
        InvokeRepeating("InstantiateCar", 1.0f, 1.6f);
        yield return new WaitForSeconds(300);
        CancelInvoke("GetData");
        
    }

    void InstantiateCar(){

        // if (carPrefab.GetComponent<MoveAgent>().status_car == 0.5)
        // {

        // }
        int azar = UnityEngine.Random.Range(0, 3);
        if (azar == 0){
            autoPrefab0.GetComponent<MoveAgent>().id = id;
            id++;
            Instantiate(autoPrefab0, new Vector3(15, 0.0f, 0), Quaternion.identity);
        }

        else if (azar == 1){
            autoPrefab1.GetComponent<MoveAgent>().id = id;
            id++;
            Instantiate(autoPrefab1, new Vector3(15, 0.0f, 0), Quaternion.identity);
        }
        
        else{
            autoPrefab2.GetComponent<MoveAgent>().id = id;
            id++;
            Instantiate(autoPrefab2, new Vector3(15, 0.0f, 0), Quaternion.identity);
        }
    }

}
