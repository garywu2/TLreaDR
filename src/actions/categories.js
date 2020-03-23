import axios from "axios";
import config from "../config/client";
import { FETCH_CATEGORIES } from './types';

export const getCategories = async () => {
    const response = await axios.get(`${config.endpoint}categories`);

    if(response.status != 200) {
        throw "Category retrieval failed with error code " + response.status;
    }

    return { type: FETCH_CATEGORIES, categories: response.data };
}