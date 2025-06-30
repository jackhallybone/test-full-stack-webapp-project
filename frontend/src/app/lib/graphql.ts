import { GraphQLClient } from "graphql-request"

const getUrl = () => {
    if (typeof window === 'undefined') {
        return process.env.GRAPHQL_SS_URL; // ie, docker container url
    } else {
        return process.env.NEXT_PUBLIC_GRAPHQL_CS_URL; // ie, localhost url
    }
};

export const graphQLClient = new GraphQLClient(getUrl(), {
    headers: {
    },
});