import heapq
import random

class ITSupportSystem:
    def __init__(self):
        self.technicians = {}
        self.tickets = []

    def add_technician(self, name, skills, workload, shift):
        self.technicians[name] = {'skills': skills, 'workload': workload, 'shift': shift, 'tickets_assigned': []}

    def add_ticket(self, id, issue_type, priority, complexity):
        self.tickets.append({'id': id, 'issue_type': issue_type, 'priority': priority, 'complexity': complexity})

    def heuristic(self, technician, ticket):
        skill_match = 1 if ticket['issue_type'] in self.technicians[technician]['skills'] else 5
        workload_factor = self.technicians[technician]['workload']
        priority_factor = ticket['priority']
        complexity_factor = ticket['complexity']
        shift_factor = 0 if self.technicians[technician]['shift'] == 'disponible' else 5
        return skill_match + workload_factor - priority_factor + complexity_factor + shift_factor

    def assign_tickets(self):
        assignments = []
        for ticket in self.tickets:
            best_tech = None
            best_score = float('inf')
            for tech in self.technicians:
                score = self.heuristic(tech, ticket)
                if score < best_score:
                    best_score = score
                    best_tech = tech
            assignments.append((ticket['id'], best_tech))
            self.technicians[best_tech]['workload'] += 1
            self.technicians[best_tech]['tickets_assigned'].append(ticket['id'])
        return assignments

    def print_technician_status(self):
        print("\nEstado de técnicos:")
        for tech, data in self.technicians.items():
            print(f"Técnico: {tech}, Carga de trabajo: {data['workload']}, Turno: {data['shift']}, Tickets asignados: {data['tickets_assigned']}")

    def resolve_ticket(self, tech_name, ticket_id):
        if ticket_id in self.technicians[tech_name]['tickets_assigned']:
            self.technicians[tech_name]['tickets_assigned'].remove(ticket_id)
            self.technicians[tech_name]['workload'] -= 1
            print(f"Ticket {ticket_id} resuelto por {tech_name}.")
        else:
            print(f"El ticket {ticket_id} no está asignado a {tech_name}.")

# Crear el sistema de soporte IT
it_support = ITSupportSystem()
it_support.add_technician('Carlos', ['Redes', 'Hardware'], 2, 'disponible')
it_support.add_technician('Ana', ['Software', 'Seguridad'], 1, 'ocupado')
it_support.add_technician('Luis', ['Bases de Datos', 'Redes'], 0, 'disponible')

# Agregar tickets de soporte
it_support.add_ticket(101, 'Software', 3, 2)
it_support.add_ticket(102, 'Redes', 2, 1)
it_support.add_ticket(103, 'Hardware', 1, 3)
it_support.add_ticket(104, 'Seguridad', 5, 4)
it_support.add_ticket(105, 'Bases de Datos', 4, 2)

# Asignar tickets a los técnicos
assignments = it_support.assign_tickets()
for ticket, technician in assignments:
    print(f"Ticket {ticket} asignado a {technician}")

# Mostrar el estado de los técnicos
it_support.print_technician_status()

# Resolver un ticket
ticket_resuelto = random.choice([101, 102, 103, 104, 105])
tech_resolviendo = random.choice(['Carlos', 'Ana', 'Luis'])
it_support.resolve_ticket(tech_resolviendo, ticket_resuelto)
