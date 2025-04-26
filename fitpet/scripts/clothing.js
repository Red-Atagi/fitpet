class Clothing {
    #clothingID; // private
    #clothingPrice;
    #clothingType;
    constructor(image_path) {
        TODO
        this.image_path = image_path;
    }


    getPrice() {
        return this.#clothingPrice;
    }


    getClothingId() {
        return this.#clothingID;
    }


    getClothingType() {
        return this.#clothingType;
    }
}

const pants = Clothing()

