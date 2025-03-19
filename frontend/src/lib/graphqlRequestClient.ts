import { GraphQLClient } from "graphql-request"

const getUrl = () => {
    if (typeof window === 'undefined') {
        return process.env.GRAPHQL_SERVER_SIDE_URL; // ie, docker container url
    } else {
        return process.env.NEXT_PUBLIC_GRAPHQL_CLIENT_SIDE_URL; // ie, localhost url
    }
};

const getToken = () => {
    return process.env.NEXT_PUBLIC_GRAPHQL_TOKEN; // or localStorage.getItem('token')
};

console.log('GraphQL URL:', getUrl());  // Log the URL to verify

export const graphqlRequestClient = new GraphQLClient(getUrl(), {
    headers: {
        Authorization: `JWT ${getToken()}`,
    },
});