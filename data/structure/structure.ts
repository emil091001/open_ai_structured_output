export default interface Structure {
    Name: string;
    ProducerName: string;
    Compliance: string[];
    ValidTo: number;
    RefYear: number;
    EPDID: string;
    environmentalImpact: TableRow[];
    additionalEnvironmentalImpact: TableRow[];
    resourceUse: TableRow[];
    endOfLifeWaste: TableRow[];
    endOfLifeFlow: TableRow[];
}

interface TableRow {
    Parameter: AllowedParameters;
    Unit: string | number;
    Values: {
        Value: string;
        Module: string;
    }[];
}

type AllowedParameters =
    | "specificString1"
    | "specificString2"
    | "specificString3"
    | boolean
    | 123.3
    | {
          hej: string;
      };

let a = 3;
