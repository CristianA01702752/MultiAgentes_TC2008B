using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using TMPro;

public class CarSpawner : MonoBehaviour
{
    private int id = 1;
    public GameObject carPrefab;
    // Start is called before the first frame update
    void Start()
    {
        InvokeRepeating("InstantiateCar", 2f, 1f);
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void InstantiateCar(){
        carPrefab.GetComponent<MoveAgent>().id = id;
        id++;
        Instantiate(carPrefab, new Vector3(10, 0.0f, 0), Quaternion.identity);
    }

}
