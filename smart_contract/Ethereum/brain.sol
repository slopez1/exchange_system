// SPDX-License-Identifier: MIT

pragma solidity >=0.5.17;

contract Brain {

    address public owner;

    struct Request{
        address requester;
        string state;
    }

    struct Asset {
        string Endpoint;
        string ID;
        address Owner;
        string Description;
        Request[] Requests;
    }

    string[] IDs;
    mapping(string => Asset) Assets;

    uint AssetsCount = 0;

    constructor() {
        owner = msg.sender;
    }

    function RequesterExists(Asset memory a, address requester) private pure returns (uint){
        for(uint i=0; i < a.Requests.length; i++){
            if(a.Requests[i].requester == requester){
                return i+1;
            }
        }
        return 0;
    }

    function AssetExists(string memory id)  public view returns (bool){
        //Return if assets is present
        return bytes(Assets[id].ID).length > 0;
    }

    function getAsset(string memory id) public view returns (Asset memory) {
        return (Assets[id]);
    }


    function getAllAssets() public view returns (Asset[] memory) {
        Asset[] memory allAssets = new Asset[](AssetsCount);
        uint index = 0;
        for (uint i = 0; i < AssetsCount; i++) {
            allAssets[index] = Assets[IDs[i]];
            index++;
        }
        return allAssets;
    }

    function createAsset(
        string memory id,
        string memory endpoint,
        string memory description
    ) public {
        require(AssetExists(id) == false, "Asset already exists");
        // Create new Asset
        //Asset storage newAsset;

        Asset storage newAsset = Assets[id];
        newAsset.Endpoint = endpoint;
        newAsset.ID = id;
        newAsset.Owner = msg.sender;
        newAsset.Description = description;

        //Add to Assets
        Assets[id]=newAsset;

        // Add to array of ids
        IDs.push(id);

        //Increment the counter
        AssetsCount = AssetsCount + 1;
    }

    function RequestAsset(string memory id) public {
        require(AssetExists(id) == true, "Asset dosen't exists"); // Check Asset exists
        uint index = RequesterExists(Assets[id], msg.sender);
        require(index == 0, "Asset already requested"); // Check requester dosen't exist
        Assets[id].Requests.push(Request(msg.sender, "Pending"));
    }

    function AcceptRequestAsset(string memory id, address requester) public {
        require(AssetExists(id) == true, "Asset dosen't exists"); // Check if Asset exists
        require(Assets[id].Owner == msg.sender, "You aren't the owner of this asset"); // Check if you are authorized to accept request
        uint index = RequesterExists(Assets[id], requester);
        require(index > 0, "Requester dosent't exists");  // Check requester exist
        Assets[id].Requests[index-1].state = "Accepted";
    }

    function DenyRequestAsset(string memory id, address requester) public {
        require(AssetExists(id) == true, "Asset dosen't exists"); // Check if Asset exists
        require(Assets[id].Owner == msg.sender, "You aren't the owner of this asset"); // Check if you are authorized to accept request
        uint index = RequesterExists(Assets[id], requester);
        require(index > 0, "Requester dosent't exists");  // Check requester exist
        Assets[id].Requests[index-1].state = "Denied";
    }

    function UpdateAsset(string memory id, string memory endpoint, string memory description) public{
        require(AssetExists(id) == true, "Asset dosen't exists"); // Check if Asset exists
        require(Assets[id].Owner == msg.sender, "You aren't the owner of this asset"); // Check if you are authorized to accept request
        Assets[id].Endpoint = endpoint;
        Assets[id].Description = description;
    }

}

